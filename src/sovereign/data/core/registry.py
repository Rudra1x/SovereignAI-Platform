"""
Simple registry implementation.

Every loader, parser, transformer,
validator will register itself here.
"""

from __future__ import annotations

from typing import Any, Dict

from .exceptions import RegistryError


class Registry:

    def __init__(self):

        self._registry: Dict[str, Any] = {}

    def register(self, name: str, component: Any):

        if name in self._registry:
            raise RegistryError(
                f"{name} already registered."
            )

        self._registry[name] = component

    def get(self, name: str):

        if name not in self._registry:
            raise RegistryError(
                f"{name} not found."
            )

        return self._registry[name]

    def exists(self, name: str):

        return name in self._registry

    def remove(self, name: str):

        if name in self._registry:
            del self._registry[name]

    def list_components(self):

        return sorted(self._registry.keys())