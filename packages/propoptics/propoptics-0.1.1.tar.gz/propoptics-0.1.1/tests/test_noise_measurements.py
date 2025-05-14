import pytest
import propoptics as po
from propoptics._propoptics import is_uniform
import numpy as np


def test_uniform():
    x = np.arange(10)
    assert is_uniform(x)
    x = np.arange(100000)
    assert is_uniform(x)
    x = np.linspace(0.0, 1.0, 10)
    assert is_uniform(x)
    x = np.linspace(0.0, 1.0, 45645)
    assert is_uniform(x)
    x = np.linspace(0.0, 87654e7, 10)
    assert is_uniform(x)

    x = np.linspace(-245e-21, 87654e7, 10)
    assert not is_uniform(x)
    x = np.linspace(-245e-21, 87654e7, 458777)
    assert not is_uniform(x)


def test_constructor_input_validation():
    with pytest.raises(ValueError):
        po.NoiseMeasurement([], [])
    with pytest.raises(ValueError):
        po.NoiseMeasurement((), ())
    with pytest.raises(ValueError):
        po.NoiseMeasurement([0.0, 1.0, 2.0], [3.0, 4.0])
    with pytest.raises(ValueError):
        po.NoiseMeasurement([0.0, 1.0, 2.0], [3.0, 4.0])
    assert po.NoiseMeasurement([0.0, 1.0, 2.0], [3.0, 4.0, 5.0])._unif
    assert not po.NoiseMeasurement([1.0, 2.0, 3.0], [3.0, 4.0, 5.0])._unif
    assert not po.NoiseMeasurement([0.0, 1.0, 4.0], [3.0, 4.0, 5.0])._unif


def test_from_time_series():
    sig = np.tile([0, 1], 1024)

    noise = po.NoiseMeasurement.from_time_series(sig)
    assert np.all(noise.psd[:-2]) < 1e-32
    noise = po.NoiseMeasurement.from_time_series(sig, nperseg=128)
    assert np.all(noise.psd[:-2]) < 1e-31

    # boxcar with pure signal has no leakage
    noise = po.NoiseMeasurement.from_time_series(sig, window="boxcar")
    assert np.all(noise.psd[:-1] == 0)
    noise = po.NoiseMeasurement.from_time_series(sig, window="boxcar", nperseg=128)
    assert np.all(noise.psd[:-1] == 0)

    sig = np.tile([-1, 0, 1, 0], 512)
    nt = len(sig)
    noise = po.NoiseMeasurement.from_time_series(sig)
    assert np.all(noise.psd[:-3]) < 1e-32
    assert noise.psd[-1] < 1e-32
    noise = po.NoiseMeasurement.from_time_series(sig, window="boxcar")
    assert tuple(np.where(noise.psd != 0)[0]) == (512,)

    # normalization: all the power is contained into one bin of size df = 1/T = 1/(nt * dt)
    assert noise.psd[512] / nt == pytest.approx(po.abs2(sig).mean())
    noise = po.NoiseMeasurement.from_time_series(sig, dt=458.200235e-15, window="boxcar")
    df = noise.freq[1]
    assert noise.psd[512] * df == pytest.approx(po.abs2(sig).mean())


def test_resampling():
    f = np.linspace(0, 0.5, 11)
    psd = f.copy()
    noise = po.NoiseMeasurement(f, psd)

    f2, psd2 = noise.sample_spectrum(21)
    assert pytest.approx(psd2[::2]) == psd
    assert pytest.approx(f2[::2]) == f

    f3, psd3 = noise.sample_spectrum(11, dt=2.0)
    assert pytest.approx(psd2[:11]) == psd3

    np.random.seed(0b10110011100011110000)
    f = np.linspace(1, 2, 11)
    psd = np.random.rand(len(f))
    noise = po.NoiseMeasurement(f, psd)
    f2, psd2 = noise.sample_spectrum(21)
    assert pytest.approx(psd2[10:]) == psd
    assert np.all(psd2[:10] == psd2[10])

    f3, psd3 = noise.sample_spectrum(21, left=0.0)
    assert np.all(f2 == f3)
    assert np.all(psd3[:10] == 0)
    assert noise.resampled(21, left=0.0)._unif

    with pytest.raises(ValueError):
        noise.sample_spectrum(11, dt=0.24)


def test_time_series():
    np.random.seed(0b10110011100011110000)
    nf = 453
    f = np.linspace(0, 1, nf)
    psd = np.random.rand(len(f))
    psd[0] = 0
    noise = po.NoiseMeasurement(f, psd)
    t, signal = noise.time_series()

    assert len(t) == len(signal) == (nf - 1) * 2
    assert pytest.approx(np.trapezoid(psd, x=f), rel=1e-2) == po.abs2(signal).mean()


def test_root_integrated():
    np.random.seed(0b10110011100011110000)
    nf = 453
    f = np.linspace(0, 1, nf)
    psd = np.random.rand(len(f))
    psd[0] = 0
    noise = po.NoiseMeasurement(f, psd)
    _, signal = noise.time_series()
    integrated = noise.root_integrated()
    assert integrated[-1] == 0
    assert pytest.approx(signal.std(), rel=1e-2) == integrated[1]
