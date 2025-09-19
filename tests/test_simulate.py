import numpy as np

import xrdplayground as xrd


def test_simulate_peak_width_vs_size():
    lat, basis = xrd.default_structure("Si")
    two_theta = np.linspace(20, 80, 3000)
    res_small = xrd.simulate_pxrd(lat, basis, energy_keV=8.0, two_theta=two_theta, size_A=50.0, hmax=3)
    res_large = xrd.simulate_pxrd(lat, basis, energy_keV=8.0, two_theta=two_theta, size_A=1000.0, hmax=3)

    # Compare width around the first significant peak
    idx_max_small = int(np.argmax(res_small.intensity))
    peak_tth = two_theta[idx_max_small]
    # measure local second moment as proxy for width
    window = (two_theta > peak_tth - 1.0) & (two_theta < peak_tth + 1.0)
    def local_width(y: np.ndarray) -> float:
        xw = two_theta[window]
        yw = y[window]
        area = float(np.trapezoid(yw, xw)) + 1e-12
        yw = yw / area
        mu = float(np.trapezoid(xw * yw, xw))
        var = float(np.trapezoid(((xw - mu) ** 2) * yw, xw))
        return np.sqrt(var)

    w_small = local_width(res_small.intensity)
    w_large = local_width(res_large.intensity)
    assert w_large < w_small, "Larger crystallite size should narrow peaks"

    # Area should be comparable (within a factor), allowing for discretization
    area_small = np.trapezoid(res_small.intensity, two_theta)
    area_large = np.trapezoid(res_large.intensity, two_theta)
    ratio = float(area_large) / (float(area_small) + 1e-12)
    assert 0.3 < ratio < 3.0
