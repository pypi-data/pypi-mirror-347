import pytest
import propoptics as po
import numpy as np

c = 299792458
TAUC = 2 * np.pi * c


def test_empty_filters():
    assert len(po.Filters.empty()) == 0
    assert po.Filters.empty().generate(np.linspace(1, 2, 21), []).shape == (0, 21)


def test_validate_product():
    with pytest.raises(ValueError):
        po.Filters([1, 2, 3], [4, 5], mode="single_pass")
    assert po.Filters([1, 2], [3, 4], mode="single_pass").positions == [1, 2]


def test_type_dimension():
    f = po.Filters([1, 2], [3, 4], mode="single_pass")
    assert len(f) == 2

    f = po.Filters([1, 2], [3, 4], mode="product")
    assert len(f) == 4

    f0 = po.Filters.empty()
    assert len(f0) == 0

    with pytest.raises(ValueError):
        po.energy_signal(np.ones((10, 10)), np.arange(12), f0)


def test_noise_signal_clean():
    f = po.Filters([1, 2], [3, 4], mode="single_pass")
    mat = np.random.rand(10, 5)
    w1 = np.linspace(-2, 2, 5)

    assert pytest.approx(po.energy_signal(mat, w1, f)[0].squeeze()[0]) == po.abs2(mat).sum(axis=1)
    f = po.Filters.empty()
    mat1 = np.ones(50)

    res, spec = po.energy_signal(mat1, np.arange(50), f)
    assert res.shape == (1, 1)
    assert res.sum() == 50

    mat2 = np.zeros((50, 50), dtype=float)
    mat2[0] = mat1
    res, spec = po.energy_signal(mat2, np.arange(50), f)
    assert res.shape == (1, 50)
    assert res[0, 0].sum() == 50


def test_noise_signal_sn():
    n = 1024
    mat = np.ones((10, n), dtype=float)
    w1, dw = np.linspace(TAUC / 10e-6, TAUC / 1e-6, n, retstep=True)
    wl = TAUC / w1
    pos = wl[2 * n // 3]
    bw = 300e-9
    mask = 4 ** (-(((wl - pos) / bw) ** 2))
    peaks = [1.0, 0.01, 0.0001]
    f = po.Filters([pos, pos, pos], [bw])

    res, spec = po.energy_signal(mat, w1, f, peaks=peaks)

    assert pytest.approx(n * dw) == res[0]  # peaks doesn't affect full spectrum
    assert pytest.approx(res[0]) == dw * po.abs2(mat).sum(axis=1)
    assert pytest.approx(res[1]) == po.abs2(mat * mask).sum(axis=1) * dw * peaks[0]
    assert pytest.approx(res[2]) == po.abs2(mat * mask).sum(axis=1) * dw * peaks[1]
    assert pytest.approx(res[3]) == po.abs2(mat * mask).sum(axis=1) * dw * peaks[2]

    mean = res.mean(axis=1)
    assert np.all(np.diff(mean) < 0)

    # attenuation increases noise, which increases variance
    assert res[1].std() / peaks[0] < res[2].std() / peaks[1] < res[3].std() / peaks[2]
