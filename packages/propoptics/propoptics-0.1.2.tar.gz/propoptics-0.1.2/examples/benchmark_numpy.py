import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import propoptics as po

h = 6.62607015e-34
hbar = 0.5 * h / np.pi


def shot_noise(w: np.ndarray, size):
    dw = w[1] - w[0]
    n = len(w)
    dt = 2 * np.pi / (dw * n)
    std = np.sqrt(0.5 * hbar * np.abs(w) / dw)
    fac = std / dt * np.sqrt(2 * np.pi)
    return fac * np.exp(2j * np.pi * np.random.rand(size, n))


def wspace(t: float | np.ndarray, t_num=0):
    """
    frequency array such that x(t) <-> np.fft(x)(w)

    Parameters
    ----------
    t : float | np.ndarray
        float : total width of the time window
        array : time array
    t_num : int-
        if t is a float, specifies the number of points

    Returns
    -------
    w : array
        linspace of frencies corresponding to t
    """
    if isinstance(t, (np.ndarray, list, tuple)):
        dt = t[1] - t[0]
        t_num = len(t)
    else:
        dt = t / t_num
    return np.fft.fftfreq(t_num, dt) * 2 * np.pi


def abs2(x):
    return x.real**2 + x.imag**2


def sum_squared(mat: np.ndarray, mask: np.ndarray) -> np.ndarray:
    return abs2(mat * mask).sum(axis=1)


def sum_squared_noise(w: np.ndarray, mat: np.ndarray, mask: np.ndarray) -> np.ndarray:
    sn = shot_noise(w, mat.shape[0])
    return abs2(mat * mask + np.sqrt(1 - mask**2) * sn).sum(axis=1)


def main():
    nx, ny = 2048, 20000
    t = np.linspace(-10, 10, nx)
    e = po.env(t, 0, 3)
    seed = np.random.rand(ny, nx)
    mat = np.exp(2j * np.pi * seed) * seed**2 * (e**2)

    tick = time.perf_counter()
    res_py = sum_squared(mat, e)
    toc_py = time.perf_counter() - tick
    print(res_py.shape, file=sys.stderr)

    tick = time.perf_counter()
    res_py_noise = sum_squared_noise(t, mat, e)
    toc_py_noise = time.perf_counter() - tick
    print(res_py_noise.shape, file=sys.stderr)

    tick = time.perf_counter()
    res_rs_inplace = po.mask_sum_inplace(mat, e)
    toc_rs_inplace = time.perf_counter() - tick
    print(res_rs_inplace.shape, file=sys.stderr)

    tick = time.perf_counter()
    res_rs = po.mask_sum(mat, e)
    toc_rs = time.perf_counter() - tick
    print(res_rs.shape, file=sys.stderr)

    tick = time.perf_counter()
    res_rs_noise = po.mask_sum_noise(t, mat, e)
    toc_rs_noise = time.perf_counter() - tick
    print(res_rs_noise.shape, file=sys.stderr)

    assert np.allclose(res_py, res_rs)
    assert np.allclose(res_rs_inplace, res_rs)

    print("python", toc_py)
    print("rust", toc_rs)
    print("rust inplace", toc_rs_inplace)
    print("python noise", toc_py_noise)
    print("rust noise", toc_rs_noise)
    print(f"speedup rs: {toc_py / toc_rs:.1f}x")
    print(f"speedup rs inplace: {toc_py / toc_rs_inplace:.1f}x")
    print(f"speedup noise rs: {toc_py_noise / toc_rs_noise:.1f}x")

    plt.plot(res_py_noise)
    plt.plot(res_rs_noise, ":")
    plt.show()


if __name__ == "__main__":
    main()
