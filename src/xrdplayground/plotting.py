from __future__ import annotations

from typing import Optional, Any
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from .models import PXRDResult


def plot_pattern(result: PXRDResult, ax: Optional[Axes] = None, **line_kwargs: Any):
    """Plot a powder XRD pattern onto a Matplotlib Axes.

    Returns the Axes used.
    """
    if ax is None:
        _, ax = plt.subplots()
    base: dict[str, Any] = {"color": "k", "lw": 1.8}
    base.update(line_kwargs)
    ax.plot(result.two_theta, result.intensity, **base)
    ax.set_xlabel("2θ (deg)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.set_xlim(result.two_theta.min(), result.two_theta.max())
    return ax
