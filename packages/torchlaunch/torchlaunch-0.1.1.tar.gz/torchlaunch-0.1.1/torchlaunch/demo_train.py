

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

from launcher import DistributedLauncher

X  = torch.randn(10_000, 32)
y  = torch.randint(0, 10, (10_000,))
dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=128, shuffle=True)

model     = nn.Sequential(nn.Linear(32, 64), nn.ReLU(), nn.Linear(64, 10))
optimizer = optim.Adam(model.parameters(), lr=3e-4)
loss_fn   = nn.CrossEntropyLoss()

launcher = DistributedLauncher(devices="auto") 

def train(lc: DistributedLauncher, num_epochs: int = 2):
    mdl, opt, dl = lc.prepare(model, optimizer, dataloader)
    device = lc.device    
    
    lc.report_gpu_usage("start") 

    for epoch in range(num_epochs):
        for xb, yb in dl:
            xb, yb = xb.to(device), yb.to(device)   # move batch!
            opt.zero_grad()
            preds = mdl(xb)
            loss  = loss_fn(preds, yb)
            lc.backward(loss)
            opt.step()

        if lc.is_main_process: 
            print(f"Epoch {epoch} — loss: {loss.item():.4f}", flush=True)

    lc.report_gpu_usage(f"epoch {epoch}")

if __name__ == "__main__":
    launcher.run(train, num_epochs=2)
