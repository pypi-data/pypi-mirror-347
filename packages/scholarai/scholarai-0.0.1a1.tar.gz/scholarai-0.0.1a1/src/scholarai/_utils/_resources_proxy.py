from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `scholarai.resources` module.

    This is used so that we can lazily import `scholarai.resources` only when
    needed *and* so that users can just import `scholarai` and reference `scholarai.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("scholarai.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
