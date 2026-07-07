from .base import BaseLoader
from .http import HTTPLoader
from .local import LocalLoader

__all__ = [
    "BaseLoader",
    "HTTPLoader",
    "LocalLoader",
]