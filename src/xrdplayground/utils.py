from __future__ import annotations

import numpy as np
from .models import Lattice


TAU = 2.0 * np.pi
DEG = np.pi / 180.0


def wavelength_from_energy_keV(energy_keV: float) -> float:
    """Convert photon energy (keV) to wavelength (Angstrom).

    lambda [A] = 12.398 / E[keV]
    """
    return 12.398 / float(energy_keV)


def q_from_two_theta(two_theta_deg: float | np.ndarray, wavelength_A: float) -> np.ndarray:
    two_theta = np.asarray(two_theta_deg, dtype=float)
    return (4.0 * np.pi / wavelength_A) * np.sin(0.5 * two_theta * DEG)


def two_theta_from_q(q: float | np.ndarray, wavelength_A: float) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    val = np.clip(q * wavelength_A / (4.0 * np.pi), -1.0, 1.0)
    return 2.0 * np.arcsin(val) / DEG


def q_hkl(lattice: Lattice, h: int, k: int, ell: int) -> float:
    """Magnitude of reciprocal vector Q for general triclinic lattice.

    Reproduces the formula used in the original app. Angles in degrees.
    Returns |Q| in 1/Angstrom.
    """
    if h == 0 and k == 0 and ell == 0:
        return 0.0
    a, b, c, alpha, beta, gamma = lattice.a, lattice.b, lattice.c, lattice.alpha, lattice.beta, lattice.gamma
    ha = h / a
    kb = k / b
    lc = ell / c
    sa = np.sin(alpha * DEG)
    ca = np.cos(alpha * DEG)
    sb = np.sin(beta * DEG)
    cb = np.cos(beta * DEG)
    sg = np.sin(gamma * DEG)
    cg = np.cos(gamma * DEG)
    num = (
        (ha * sa) ** 2
        + (kb * sb) ** 2
        + (lc * sg) ** 2
        + 2.0 * ha * kb * (ca * cb - cg)
        + 2.0 * ha * lc * (ca * cg - cb)
        + 2.0 * kb * lc * (cb * cg - ca)
    )
    den = 1.0 - ca * ca - cb * cb - cg * cg + 2.0 * ca * cb * cg
    return np.sqrt(num / den) * TAU


def gaussian_on_axis(x: np.ndarray, center: float, sigma: float) -> np.ndarray:
    if sigma <= 0:
        # Dirac-like: put a very sharp peak
        sigma = max(1e-6, 0.01 * (x[1] - x[0]))
    return (1.0 / (np.sqrt(2.0 * np.pi) * sigma)) * np.exp(-0.5 * ((x - center) / sigma) ** 2)


def scherrer_sigma_2theta(two_theta_deg: float, wavelength_A: float, crystallite_size_A: float) -> float:
    """Return sigma (standard deviation) in degrees from Scherrer broadening.

    Original app used: 0.9 * lambda / (2.355 * D * cos(theta)) and then used that as sigma directly.
    Here we follow the same so results match the legacy behavior.
    """
    theta = 0.5 * two_theta_deg * DEG
    if crystallite_size_A is None or crystallite_size_A <= 0:
        return 0.05  # fallback small width in degrees
    return 0.9 * wavelength_A / (2.355 * crystallite_size_A * np.cos(theta)) * (180.0 / np.pi)
