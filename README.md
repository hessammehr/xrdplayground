# XRDplayground

Notebook-friendly X-ray powder diffraction utilities. This refactors the original Qt GUI into a clean Python library you can import in Jupyter or marimo.

- No Qt or i18n; pure compute + plotting helpers
- Typed models and a small, clean API
- Python 3.13+


## Quick start with `marimo`

```sh
uvx --with-editable . marimo edit --watch examples
```

## API overview

- list_structures() -> list of preset names
- default_structure(name) -> (Lattice, Basis)
- simulate_pxrd(lattice, basis, energy_keV, two_theta, size_A=..., hmax=4) -> PXRDResult
- plot_pattern(result, ax=None, **kwargs) -> Axes

## Tests

```sh
uvx run --with-editable . pytest
```

## Next steps

- Peak list extraction with HKL labeling alongside simulated pattern
- Optional Lorentz–polarization and Debye–Waller factors
- CIF import helper for lattice/basis
- Performance: symmetry-aware HKL enumeration, vectorized F(hkl)

## License

Apache-2.0
