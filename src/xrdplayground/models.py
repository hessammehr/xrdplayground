from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import numpy as np


@dataclass(frozen=True)
class Atom:
    element: str
    position: tuple[float, float, float]  # fractional coordinates in [0,1)
    b_iso: float | None = None            # isotropic displacement (optional)


@dataclass(frozen=True)
class Basis:
    atoms: tuple[Atom, ...]

    @staticmethod
    def from_lists(elements: Sequence[str], positions: Sequence[Sequence[float]]) -> "Basis":
        if len(elements) != len(positions):
            raise ValueError("elements and positions must have the same length")
        atoms = []
        for e, p in zip(elements, positions):
            if len(p) != 3:
                raise ValueError("each position must have 3 fractional coords (x, y, z)")
            x, y, z = (float(p[0]), float(p[1]), float(p[2]))
            atoms.append(Atom(e, (x, y, z)))
        atoms = tuple(atoms)
        return Basis(atoms)


@dataclass(frozen=True)
class Lattice:
    a: float
    b: float
    c: float
    alpha: float  # degrees
    beta: float   # degrees
    gamma: float  # degrees

    def as_array(self) -> np.ndarray:
        return np.asarray([self.a, self.b, self.c, self.alpha, self.beta, self.gamma], dtype=float)


@dataclass(frozen=True)
class PXRDResult:
    two_theta: np.ndarray
    intensity: np.ndarray
    hkl: list[tuple[int, int, int]] | None = None

    def copy_with(self, *, two_theta=None, intensity=None) -> "PXRDResult":
        return PXRDResult(
            two_theta=self.two_theta if two_theta is None else two_theta,
            intensity=self.intensity if intensity is None else intensity,
            hkl=self.hkl,
        )
