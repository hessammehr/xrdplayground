from __future__ import annotations

from .models import Lattice, Basis


_STRUCTURES: dict[str, tuple[Lattice, Basis]] = {
    "LaB6": (
        Lattice(4.155, 4.155, 4.155, 90.0, 90.0, 90.0),
        Basis.from_lists(
            ["La", "B", "B", "B", "B", "B", "B"],
            [
                (0.0, 0.0, 0.0),
                (0.1996, 0.5, 0.5),
                (0.5, 0.5, 0.8004),
                (0.5, 0.5, 0.1996),
                (0.5, 0.1996, 0.5),
                (0.5, 0.8004, 0.5),
                (0.8004, 0.5, 0.5),
            ],
        ),
    ),
    "Si": (
        Lattice(5.43, 5.43, 5.43, 90.0, 90.0, 90.0),
        Basis.from_lists(
            ["Si"] * 8,
            [
                (0.0, 0.0, 0.0),
                (0.5, 0.5, 0.0),
                (0.0, 0.5, 0.5),
                (0.5, 0.0, 0.5),
                (0.25, 0.25, 0.25),
                (0.75, 0.75, 0.25),
                (0.75, 0.25, 0.75),
                (0.25, 0.75, 0.75),
            ],
        ),
    ),
    "Diamond": (
        Lattice(3.56, 3.56, 3.56, 90.0, 90.0, 90.0),
        Basis.from_lists(
            ["C"] * 8,
            [
                (0.0, 0.0, 0.0),
                (0.5, 0.5, 0.0),
                (0.0, 0.5, 0.5),
                (0.5, 0.0, 0.5),
                (0.25, 0.25, 0.25),
                (0.75, 0.75, 0.25),
                (0.75, 0.25, 0.75),
                (0.25, 0.75, 0.75),
            ],
        ),
    ),
    "NaCl": (
        Lattice(5.63, 5.63, 5.63, 90.0, 90.0, 90.0),
        Basis.from_lists(
            ["Cl", "Cl", "Cl", "Cl", "Na", "Na", "Na", "Na"],
            [
                (0.0, 0.0, 0.0),
                (0.5, 0.5, 0.0),
                (0.5, 0.0, 0.5),
                (0.0, 0.5, 0.5),
                (0.5, 0.5, 0.5),
                (0.5, 0.0, 0.0),
                (0.0, 0.5, 0.0),
                (0.0, 0.0, 0.5),
            ],
        ),
    ),
    "CsCl": (
        Lattice(4.11, 4.11, 4.11, 90.0, 90.0, 90.0),
        Basis.from_lists(
            ["Cl", "Cs"],
            [
                (0.0, 0.0, 0.0),
                (0.5, 0.5, 0.5),
            ],
        ),
    ),
}


def list_structures() -> list[str]:
    return sorted(_STRUCTURES.keys())


def default_structure(name: str) -> tuple[Lattice, Basis]:
    try:
        return _STRUCTURES[name]
    except KeyError as e:
        raise KeyError(f"Unknown structure '{name}'. Available: {', '.join(list_structures())}") from e
