import propoptics as po
import numpy as np
import pytest

c = 299792458.0
TAUC = 2 * np.pi * c


def test_jitter_calculation():
    n = 1024
    mat = np.ones((10, n), dtype=complex)
    w1, dw = np.linspace(TAUC / 10e-6, TAUC / 1e-6, n, retstep=True)
    dt = 1 / (dw * 0.5 / np.pi * len(w1))

    # if the spectrum is perfectly flat, we get one spike in the time domaine
    jitter, _ = po.jitter_signal(mat, w1)

    assert dt * n / 2 == pytest.approx(-jitter[0, 0])

    t = np.arange(-n / 2 * dt, n / 2 * dt, dt)

    n_rows = 200
    delays = np.random.randn(n_rows) * 2 * dt
    mat = np.ones((n_rows, n), dtype=complex)
    for row, off in zip(mat, delays):
        row[:] = np.fft.fft(4 ** (-(((t - off) / (15 * dt)) ** 2)))
    jitter, _ = po.jitter_signal(mat, w1)

    assert jitter.std() == pytest.approx(2 * dt, rel=1e-2)


if __name__ == "__main__":
    test_jitter_calculation()
