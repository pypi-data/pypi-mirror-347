# jaxflow/__init__.py

"""
JAXFlow
=======

A lightweight, Flax-style neural-network library built on JAX.
"""

from __future__ import annotations
from importlib import metadata as _metadata
from typing import TYPE_CHECKING as _TYPE_CHECKING

# ---------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------
try:
    __version__: str = _metadata.version("jaxflow")
except _metadata.PackageNotFoundError:  # editable install
    __version__ = "0.0.0+dev"
del _metadata


# ---------------------------------------------------------------------
# Lazy-loaded sub-packages (heavy deps only on access)
# ---------------------------------------------------------------------
import importlib, types as _types

__lazy_subpackages = {
    "activations",
    "callbacks",
    "initializers",
    "layers",
    "losses",
    "math",
    "metrics",
    "models",
    "nn",
    "optimizers",
    "random",
    "regularizers",
    "core",
    "gradient",
}

def __getattr__(name: str) -> _types.ModuleType:
    if name in __lazy_subpackages:
        mod = importlib.import_module(f".{name}", __name__)
        globals()[name] = mod   # cache on first access
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# ---------------------------------------------------------------------
# Help static type checkers know about our lazy modules
# ---------------------------------------------------------------------
if _TYPE_CHECKING:
    from . import (
        activations,
        callbacks,
        core,
        gradient,
        initializers,
        layers,
        losses,
        math,
        metrics,
        models,
        nn,
        optimizers,
        random,
        regularizers,
        

    )

# ---------------------------------------------------------------------
# What shows up on `from jaxflow import *`
# ---------------------------------------------------------------------
__all__ = [
    
    # subpackages
    *sorted(__lazy_subpackages),
    # meta
    "__version__",
]
