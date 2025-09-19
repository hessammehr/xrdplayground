import math
import numpy as np

from xrdplayground.models import Lattice
from xrdplayground.utils import q_hkl, q_from_two_theta, two_theta_from_q


def test_q_hkl_cubic_matches_analytic():
    # cubic lattice: |Q| = 2π/a * sqrt(h^2 + k^2 + l^2)
    a = 5.0
    lat = Lattice(a, a, a, 90.0, 90.0, 90.0)

    def analytic(h, k, ell):
        return 2.0 * math.pi / a * math.sqrt(h * h + k * k + ell * ell)

    for hkl in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 1, 1), (2, 0, 0)]:
        q_num = q_hkl(lat, *hkl)
        q_ref = analytic(*hkl)
        assert math.isclose(q_num, q_ref, rel_tol=1e-12, abs_tol=1e-12)


def test_two_theta_q_roundtrip():
    wl = 1.5406  # Cu Kα approx.
    tth = np.array([10.0, 30.0, 60.0])
    q = q_from_two_theta(tth, wl)
    tth2 = two_theta_from_q(q, wl)
    assert np.allclose(tth, tth2, atol=1e-9)
