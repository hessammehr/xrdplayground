# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "matplotlib==3.10.6",
#     "numpy==2.3.3",
# ]
# ///
import marimo

__generated_with = "0.16.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import xrdplayground as xrd

    from matplotlib import pyplot as plt
    return mo, np, plt, xrd


@app.cell
def _(mo, np, xrd):
    lat, basis = xrd.default_structure("Si")
    two_theta = np.linspace(5, 65, 2000)
    energy = mo.ui.slider(4.0, 25.0, value=8.0, step=0.1, label="Energy (keV)")
    size = mo.ui.slider(10.0, 2000.0, value=500.0, step=10.0, label="Crystallite size (Å)")
    hmax = mo.ui.slider(1, 8, value=4, step=1, label="HKL max (±h,k,l)")
    return basis, energy, hmax, lat, size, two_theta


@app.cell
def _(basis, lat, two_theta, xrd):
    def simulate(energy_keV: float, size_A: float, hmax_v: int):
        return xrd.simulate_pxrd(lat, basis, energy_keV=energy_keV, two_theta=two_theta, size_A=size_A, hmax=hmax_v)
    return (simulate,)


@app.cell
def _(energy, hmax, mo, plt, simulate, size, xrd):
    result = simulate(energy.value, size.value, int(hmax.value))

    fig, ax = plt.subplots(figsize=(12,12))
    xrd.plot_pattern(result, ax=ax)
    ax.set_title(f"Si | E={energy.value:.2f} keV, D={size.value:.0f} Å, hmax=±{int(hmax.value)}")

    mo.vstack([
        mo.hstack([energy, size, hmax]),
        fig,
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
