from importlib.metadata import version as _v
from .launcher import DistributedLauncher, launch   # re-export

__all__ = ["DistributedLauncher", "launch"]
__version__ = _v(__name__)
