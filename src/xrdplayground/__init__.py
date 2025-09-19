"""
XRD Playground (library)

A minimal, notebook-first refactor of the original Qt app. This package exposes
pure functions and light objects to compute powder XRD patterns from lattice
parameters and atomic bases, using xrayutilities for scattering factors.

Highlights:
- No Qt, no i18n, just core computation + plotting helpers.
- Python 3.13+ only.
- Stable, typed API designed for Jupyter/marimo workflows.

Top-level API:
- simulate_pxrd(params: Lattice, basis: Basis, energy_keV: float, two_theta: np.ndarray, size_A: float | None) -> PXRDResult
- default_structure(name: str) -> tuple[Lattice, Basis]
- list_structures() -> list[str]
- plot_pattern(result: PXRDResult, ax: matplotlib.axes.Axes | None = None)
"""

from .models import Atom, Basis, Lattice, PXRDResult
from .structures import list_structures, default_structure
from .simulate import simulate_pxrd
from .plotting import plot_pattern

__all__ = [
    "Atom",
    "Basis",
    "Lattice",
    "PXRDResult",
    "list_structures",
    "default_structure",
    "simulate_pxrd",
    "plot_pattern",
]
