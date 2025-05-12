from __future__ import annotations
import os, torch
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union

import torch.distributed as dist
import torch.multiprocessing as mp
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler

__all__ = ["DistributedLauncher", "launch"]


@dataclass
class _DistState:
    world_size: int = 1
    rank: int = 0
    local_rank: int = 0
    device: torch.device = torch.device("cpu")

    @property
    def is_main(self) -> bool:
        return self.rank == 0


class DistributedLauncher:
    def __init__(
        self,
        *,
        devices: Union[int, Sequence[int], str] = "auto",
        backend: Optional[str] = None,
        num_nodes: int = 1,
        node_rank: int = 0,
        master_addr: str = "127.0.0.1",
        master_port: int = 29500,
        strategy: str = "ddp",
    ) -> None:
        self.devices = self._resolve_devices(devices)
        self.backend = backend or ("nccl" if torch.cuda.is_available() else "gloo")
        self.num_nodes = num_nodes
        self.node_rank = node_rank
        self.master_addr = master_addr
        self.master_port = master_port
        self.strategy = strategy.lower()

        self._state: _DistState = _DistState()

    @property
    def rank(self) -> int: return self._state.rank
    @property
    def world_size(self) -> int: return self._state.world_size
    @property
    def is_main_process(self) -> bool: return self._state.is_main
    @property
    def device(self) -> torch.device: return self._state.device

    def backward(self, loss: torch.Tensor) -> None:
        loss.backward()

    def run(self, train_fn: Callable[..., None], *args: Any, **kwargs: Any) -> None:
        """Decide between single-process and multi-GPU spawn."""
        if len(self.devices) == 0:          # CPU-only
            self._init_single_process(None)
            train_fn(self, *args, **kwargs)
            self._finalize()
            return

        world = len(self.devices) * self.num_nodes
        if world == 1:                      # single GPU
            self._init_single_process(self.devices[0])
            train_fn(self, *args, **kwargs)
            self._finalize()
            return

        mp.spawn(
            self._worker,
            args=(train_fn, args, kwargs),
            nprocs=len(self.devices),
            join=True,
        )

    def prepare(
        self,
        model: torch.nn.Module,
        optimizer: Optional[torch.optim.Optimizer] = None,
        dataloader: Optional[DataLoader] = None,
    ) -> Tuple[torch.nn.Module, Optional[torch.optim.Optimizer], Optional[DataLoader]]:
        if not dist.is_initialized():       # single process
            return model.to(self.device), optimizer, dataloader

        device = self.device
        if torch.cuda.is_available():
            torch.cuda.set_device(device)
        model = model.to(device)

        if dataloader and not isinstance(dataloader.sampler, DistributedSampler):
            sampler = DistributedSampler(dataloader.dataset, shuffle=getattr(dataloader, "shuffle", True))
            dataloader = DataLoader(
                dataloader.dataset,
                batch_size=dataloader.batch_size,
                shuffle=False,
                num_workers=dataloader.num_workers,
                pin_memory=dataloader.pin_memory,
                sampler=sampler,
            )

        if self.strategy == "ddp" and self.world_size > 1:
            model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[device.index] if torch.cuda.is_available() else None)
        return model, optimizer, dataloader

    _verbose: bool = True

    @staticmethod
    def _resolve_devices(devices: Union[int, Sequence[int], str]) -> List[int]:
        if devices in ("all", "auto"):
            return list(range(torch.cuda.device_count())) if torch.cuda.is_available() else []
        if isinstance(devices, int):
            return list(range(min(devices, torch.cuda.device_count()))) if devices > 0 else []
        return list(devices)

    def _worker(
        self,
        local_rank: int,
        train_fn: Callable[..., None],
        args: Tuple[Any, ...],
        kwargs: dict,
    ) -> None:
        global_rank = self.node_rank * len(self.devices) + local_rank
        world_size  = self.num_nodes * len(self.devices)

        os.environ.update(
            {
                "MASTER_ADDR": self.master_addr,
                "MASTER_PORT": str(self.master_port),
                "RANK":        str(global_rank),
                "WORLD_SIZE":  str(world_size),
                "LOCAL_RANK":  str(local_rank),
            }
        )

        self._init_distributed(local_rank, global_rank, world_size)

        dist.barrier(device_ids=[local_rank] if self.backend == "nccl" else None)

        try:
            train_fn(self, *args, **kwargs)    # ← pass *this* launcher
        finally:
            self._finalize()

    def _init_single_process(self, device_idx: Optional[int]) -> None:
        self._state.rank = 0
        self._state.world_size = 1
        dev = torch.device("cuda", device_idx) if (device_idx is not None and torch.cuda.is_available()) else torch.device("cpu")
        self._state.device = dev
        if dev.type == "cuda":
            torch.cuda.set_device(dev)

    def _init_distributed(self, local_rank: int, global_rank: int, world_size: int) -> None:
        dist.init_process_group(backend=self.backend, rank=global_rank, world_size=world_size)
        self._state.rank = global_rank
        self._state.local_rank = local_rank
        self._state.world_size = world_size
        self._state.device = torch.device("cuda", local_rank) if torch.cuda.is_available() else torch.device("cpu")
        if torch.cuda.is_available():
            torch.cuda.set_device(self._state.device)

    def _finalize(self) -> None:
        if dist.is_initialized():
            dist.barrier()
            dist.destroy_process_group()
    
    def report_gpu_usage(self, label: str = "") -> None:
        if not self.is_main_process:
            return

        import torch
        hdr = f"[GPU-REPORT {label}] " if label else "[GPU-REPORT] "
        total = torch.cuda.device_count()
        used  = len(self.devices)

        print(f"{hdr}{used} of {total} visible GPUs in use.")

        for idx in range(used):
            props = torch.cuda.get_device_properties(idx)
            mem_total = props.total_memory / 1024**3
            mem_alloc = torch.cuda.memory_allocated(idx) / 1024**3
            pct = (mem_alloc / mem_total) * 100
            line = f"  • GPU {idx}: {mem_alloc:.2f} / {mem_total:.2f} GiB  ({pct:5.1f}% alloc)"
            try:
                from pynvml import (
                    nvmlInit,
                    nvmlDeviceGetHandleByIndex,
                    nvmlDeviceGetUtilizationRates,
                )
                nvmlInit()
                util = nvmlDeviceGetUtilizationRates(
                    nvmlDeviceGetHandleByIndex(idx)
                ).gpu
                line += f", {util:3d}% compute util"
            except Exception:
                # pynvml not installed or failed → skip compute util
                pass
            print(line, flush=True)


def launch(train_fn: Callable[..., None], *args: Any, **kwargs: Any) -> None:
    DistributedLauncher(devices="auto").run(train_fn, *args, **kwargs)
