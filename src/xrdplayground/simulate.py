from __future__ import annotations

from typing import List, Tuple
import numpy as np
import xrayutilities as xu

from .models import Lattice, Basis, PXRDResult
from .utils import (
    wavelength_from_energy_keV,
    q_from_two_theta,
    two_theta_from_q,
    q_hkl,
    gaussian_on_axis,
    scherrer_sigma_2theta,
)


def _structure_factor_squared(
    basis: Basis, hkl: Tuple[int, int, int], q: float, energy_keV: float
) -> float:
    """Compute |F(hkl)|^2 using xrayutilities atomic form factors.

    energy is in keV, converted to eV for f1/f2.
    """
    en_eV = float(energy_keV) * 1000.0
    h, k, ell = hkl
    F = 0.0 + 0.0j
    for atom in basis.atoms:
        # Resolve element symbol in xrayutilities materials library
        try:
            elem = getattr(xu.materials.elements, atom.element)
        except AttributeError as e:
            raise ValueError(f"Unknown element symbol '{atom.element}' for xrayutilities") from e
        f = elem.f0(q) + elem.f1(en_eV) + 1j * elem.f2(en_eV)
        phase = -2.0 * np.pi * 1j * (h * atom.position[0] + k * atom.position[1] + ell * atom.position[2])
        F += f * np.exp(phase)
    return float(np.abs(F) ** 2)


def _enumerate_hkls(hmax: int, kmax: int | None = None, lmax: int | None = None) -> List[Tuple[int, int, int]]:
    if kmax is None:
        kmax = hmax
    if lmax is None:
        lmax = hmax
    hkls: list[tuple[int, int, int]] = []
    for h in range(-hmax, hmax + 1):
        for k in range(-kmax, kmax + 1):
            for ell in range(-lmax, lmax + 1):
                if h == 0 and k == 0 and ell == 0:
                    continue
                hkls.append((h, k, ell))
    return hkls


def simulate_pxrd(
    params: Lattice,
    basis: Basis,
    energy_keV: float,
    two_theta: np.ndarray,
    size_A: float | None = 500.0,
    hmax: int = 4,
) -> PXRDResult:
    """Simulate a powder XRD pattern.

    Inputs:
    - params: Lattice parameters (a,b,c,alpha,beta,gamma)
    - basis: Basis atoms with fractional positions
    - energy_keV: incident energy in keV
    - two_theta: ndarray of 2θ values in degrees
    - size_A: Scherrer crystallite size in Angstrom (None to disable broadening)
    - hmax: max HKL index magnitude (±hmax) for h, k, l

    Returns: PXRDResult(two_theta, intensity)
    """
    two_theta = np.asarray(two_theta, dtype=float)
    wl = wavelength_from_energy_keV(energy_keV)
    q_min = float(q_from_two_theta(two_theta.min(), wl))
    q_max = float(q_from_two_theta(two_theta.max(), wl))

    # Build candidate HKLs within Q window
    intensity = np.zeros_like(two_theta, dtype=float)
    hkls = _enumerate_hkls(hmax)
    for h, k, ell in hkls:
        q = q_hkl(params, h, k, ell)
        if not (q_min < q < q_max):
            continue
        F2 = _structure_factor_squared(basis, (h, k, ell), q, energy_keV)
        tth_peak = float(two_theta_from_q(q, wl))
        sigma = scherrer_sigma_2theta(tth_peak, wl, size_A if size_A is not None else 0.0)
        intensity += (F2 / (q * q)) * gaussian_on_axis(two_theta, tth_peak, sigma)

    return PXRDResult(two_theta=two_theta, intensity=intensity, hkl=None)
