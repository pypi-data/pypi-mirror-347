from pathlib import Path

import matplotlib.pyplot as plt
import propoptics as po
import numpy as np

TAUC = 2 * np.pi * 299792458.0
HBAR = 1.054571818e-34


def gaussian_envelope(t: np.ndarray, t_fwhm: float):
    """Generate a gaussian AMPLITUDE envelope

    Parameters
    ----------
    t : np.ndarray
        time grid
    t_fwhm : float
        full width at half maximum of the INTENSITY profile

    Returns
    -------
    np.ndarray
        amplitude envelope

    """

    return np.exp(-((t * np.sqrt(2 * np.log(2)) / t_fwhm) ** 2))


def scale_wavelength_intensity(lambda_: np.ndarray, spectrum: np.ndarray) -> np.ndarray:
    """returns an intensity profile such that, when plotted against wavelengths, the
    total energy is conserved

    Parameters
    ----------
    lambda_ : np.ndarray
        wavelengths grid
    spectrum : np.ndarray
        AMPLITUDE

    Returns
    -------
    np.ndarray
        intensity profile

    """
    return TAUC / (lambda_**2) * po.abs2(np.fft.fftshift(spectrum))


def shot_noise(w: np.ndarray) -> np.ndarray:
    """
    Parameters
    ----------
    w : np.ndarray
        angular frequencies

    Returns
    -------
    np.ndarray, shape (n,)
        noise spectrum, scaled such that |`ifft(shot_noise(w))`|^2 represents
        instantaneous power in W.
    """
    n = len(w)
    dw = abs(w[1] - w[0])
    dt = 2 * np.pi / (dw * n)
    std = np.sqrt(0.5 * HBAR * np.abs(w[0]) / dw)
    fac = std / dt * np.sqrt(2 * np.pi)
    real = np.random.randn(n) * np.sqrt(0.5)
    imag = np.random.randn(n) * np.sqrt(0.5) * 1j
    return fac * (real + imag)


def main():
    nperseg = 128
    nsegments = 50
    nt = (nperseg // 2) * nsegments

    mean_peak_power = 30e3  # 30kW

    # 2ps optical window
    optical_time, dt_opt = np.linspace(-1e-12, 1e-12, 512, retstep=True)

    # Angular frequency for pump centered at 800nm
    omega = 2 * np.pi * np.fft.fftfreq(len(optical_time), d=dt_opt) + TAUC / 800e-9
    lambda_ = np.fft.fftshift(TAUC / omega)  # for plotting

    time_envelopes = np.zeros((nt, len(optical_time)), dtype=complex)

    # load a PSD measurement
    freq, rin_psd = np.load(Path(__file__).parent / "rin_psd.npy")

    # Uncomment to simulate noise close to shot-noise limit:
    rin_psd *= 2e-4

    init_noise = po.NoiseMeasurement(freq, rin_psd)

    # generate a time series based on PSD
    # set rng seed for reproducibility
    slow_time, noise_signal = init_noise.time_series(nt=nt, rng=123456789)

    _, ax = plt.subplots(constrained_layout=True)
    ax.plot(1e6 * slow_time, 100 * noise_signal, marker=".", ls="")
    ax.set_xlabel("slow time (us)")
    ax.set_ylabel("variation from mean (%)")
    plt.show()

    _, ax = plt.subplots(constrained_layout=True)
    for offset, time_env in zip(noise_signal, time_envelopes):
        # `offset` is an element of `noise_signal`, which represent variation around a mean pulse
        # energy. If we don't consider variations in pulse durations, `mean_peak_power * (1+offset)`
        # gives the peak power of an individual pulse.
        time_env[:] = np.sqrt(mean_peak_power * (1 + offset)) * gaussian_envelope(
            optical_time, 50e-15
        )
        time_env[:] += np.fft.ifft(shot_noise(omega))

        ax.plot(1e15 * optical_time, 1e-3 * po.abs2(time_env), c="0.8", lw=0.5)
    ax.plot(1e15 * optical_time, 1e-3 * po.abs2(time_envelopes).mean(axis=0), c="red")
    ax.set_xlabel("optical time (fs)")
    ax.set_ylabel("inst. power (kW)")
    plt.show()

    #  -----------
    #  Propagation omitted
    #  -----------

    filter_wavelengths = [800e-9, 810e-9]
    filters = po.Filters(filter_wavelengths, 10e-9)
    init_spectra = np.fft.fft(time_envelopes)
    energies, spectra = po.energy_signal(init_spectra, omega, filters)

    _, (top, bottom) = plt.subplots(2, 1, figsize=(13, 8), constrained_layout=True)
    bottom.plot(*init_noise.plottable(), label="Input", c="k")
    for spectrum, energy, label in zip(
        [init_spectra[0]] + list(spectra),
        energies,
        ["No filtering"] + [f"{wl * 1e9:.0f}nm" for wl in filter_wavelengths],
    ):
        (line,) = top.plot(lambda_ * 1e9, scale_wavelength_intensity(lambda_, spectrum))

        noise_signal = energy / energy.mean() - 1.0
        noise = po.NoiseMeasurement.from_time_series(noise_signal, init_noise.dt, nperseg=nperseg)

        bottom.plot(*noise.plottable(), label=label, c=line.get_color())
    bottom.legend()
    bottom.set_xscale("log")

    top.set_xlim(700, 900)
    plt.show()


if __name__ == "__main__":
    main()
