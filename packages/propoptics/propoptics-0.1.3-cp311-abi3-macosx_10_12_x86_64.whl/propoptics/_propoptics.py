from __future__ import annotations

import importlib.metadata
import itertools
from dataclasses import dataclass
from typing import Iterator, Literal, Self, Sequence

import numpy as np
import scipy.signal as sci_sig
from scipy.integrate import cumulative_trapezoid

import propoptics._lib_propoptics as rs
from propoptics.math import to_dB  # noqa: F401

__version__ = importlib.metadata.version("propoptics")
del importlib

VALID_MODES = {"product", "single_pass"}
h = 6.62607015e-34
c = 299792458.0
hbar = 0.5 * h / np.pi
TAUC = c * 6.2831853071796
FWHM_TO_T0 = 1 / (np.sqrt(2 * np.log(2)))


@dataclass(init=False)
class Filters:
    positions: list[float]
    bandwidths: list[float]
    mode: Literal["product", "single_pass"] = "product"

    def __init__(
        self,
        positions: list[float] | float,
        bandwidths: list[float] | float,
        mode: Literal["product", "single_pass"] = "product",
    ):
        """Create a set of bandpass filters

        Parameters
        ----------
        positions : list[float] | float
            central wavelength(s) (in m) of the bandpass filters
        positions : list[float] | float
            -3dB bandwidth(s)/FWHM (in m) of the bandpass filters
        mode
            `product`: iterating through the filters yields every possible combination of wavelength
                       and bandwidth (default)
            `single_pass`: iterating through the filters is done in parallel like `zip`.
        """

        if mode not in VALID_MODES:
            raise ValueError(f"mode must be one of {VALID_MODES!r}, got {mode!r}")
        if isinstance(positions, (float, int, np.floating, np.integer)):
            positions = [positions]
        if isinstance(bandwidths, (float, int, np.floating, np.integer)):
            bandwidths = [bandwidths]

        self.positions = positions
        self.bandwidths = bandwidths
        self.mode = mode
        if self.mode == "single_pass" and (len(self.positions) != len(self.bandwidths)):
            raise ValueError(
                "`single_pass` mode requires positions and bandwidths to be the same size,"
                f"got ({len(self.positions)}, {len(self.bandwidths)})"
            )

    def __len__(self):
        return len(self.positions) * (1 if self.mode == "single_pass" else len(self.bandwidths))

    def __iter__(self) -> Iterator[tuple[float, float]]:
        if self.mode == "single_pass":
            return zip(self.positions, self.bandwidths)
        else:
            return itertools.product(self.positions, self.bandwidths)

    @classmethod
    def empty(cls) -> Self:
        return cls([], [])

    def generate(self, wl: np.ndarray, peaks: np.ndarray | Sequence[float]) -> np.ndarray:
        """
        Generates gaussian windows matching the characteristics of the filters

        Parameters
        ----------
        wl : np.ndarray, shape (n,)
            wavelength grid
        peaks : Sequence[float], len(peaks) == len(self)
            peak of each bandpass filter, (should be a sequence of `1` for no constant attenuation)

        Returns
        -------
        np.ndarray, shape (len(self), n)
            bandpass windows
        """
        assert len(peaks) == len(self), "peaks and filters must have the same length"
        out = np.zeros((len(self), len(wl)), dtype=float)
        for i, ((p, b), peak) in enumerate(zip(self, peaks)):
            out[i] = np.sqrt(peak) * np.exp(-(((wl - p) / (FWHM_TO_T0 * b)) ** 2))
        return out


class NoiseMeasurement:
    freq: np.ndarray
    psd: np.ndarray
    _unif: bool

    def __init__(self, freq: np.ndarray, psd: np.ndarray):
        """Creates a noise measurement based on a PSD

        Parameters
        ----------
        freq : np.ndarray
            equally spaces frequency array
        psd : np.ndarray
            noise power spectral density, one-sided, in linear scale, relative to carrier signal

        """
        freq = np.asarray(freq)
        psd = np.asarray(psd)
        if freq.ndim != 1 or psd.ndim != 1 or len(freq) != len(psd) or len(freq) == 0:
            raise ValueError(
                "`freq` and `psd` must be 1-d arrays of the same length"
                f"got {freq.shape=}, {psd.shape=}"
            )
        if any(freq < 0):
            raise ValueError("Only positive frequency PSDs are supported")
        if any(psd < 0):
            raise ValueError(
                "Power spectral density cannot be negative. Are you using the correct scale?"
            )

        self.freq = freq
        self.psd = psd
        self._unif = is_uniform(freq)

    def __repr__(self) -> str:
        unif = "uniformly " if self._unif else ""
        return f"<{self.__class__.__name__} {len(self.freq)} {unif}sampled points>"

    def __len__(self) -> int:
        return len(self.freq)

    @classmethod
    def from_dBc(cls, freq: np.ndarray, psd_dBc: np.ndarray) -> NoiseMeasurement:
        """Build a NoiseMeasurement from a measurement file in dBc

        Parameters
        ----------
        freq : np.ndarray
            frequency array
        psd_dBm : np.ndarray
            noise data in dBc, i.e. log10(noise signal / DC signal)

        Returns
        -------
        NoiseMeasurement

        """
        psd = 10 ** (psd_dBc / 10)
        return cls(freq, psd)

    @classmethod
    def from_dBm(
        cls, freq: np.ndarray, psd_dBm: np.ndarray, ref: float, impedence: float = 50.0
    ) -> NoiseMeasurement:
        """Build a NoiseMeasurement from a measurement file in dBm

        Parameters
        ----------
        freq : np.ndarray
            frequency array
        psd_dBm : np.ndarray
            noise data in dBm (i.e. 10 * log10(mW/1mW))
        ref : float
            reference voltage, i.e. mean voltage of the DC signal, in V
        impedence : float
            impedence of the signal chain, by default 50 Ohm

        Returns
        -------
        NoiseMeasurement

        """
        ref_dB = 10 * np.log10(ref**2 / impedence * 1000)
        psd = 10 ** ((psd_dBm - ref_dB) / 10)
        return cls(freq, psd)

    @classmethod
    def from_time_series(
        cls,
        signal: np.ndarray | Sequence[float],
        dt: float = 1.0,
        window: str | None = "hann",
        nperseg: int | None = None,
        nf: int | None = None,
        detrend: bool | str = "constant",
    ) -> NoiseMeasurement:
        """
        compute a PSD estimation from a time-series measurement.

        Parameters
        ----------
        time : np.ndarray, shape (n,)
            time axis, must be uniformly spaced
        signal : np.ndarray, shape (n,)
            signal to process. You may or may not remove the DC component, as this will only affect
            the 0 frequency bin of the PSD
        window : str | None, optional
            refer to scipy.signal.welch for possible windows
        nperseg : int, optional
            number of points per segment. The PSD of each segment is computed and then averaged
            to reduce variange. By default None, which means only one segment (i.e. the full signal
            at once) is computed.
        nf : int, optional
            specify the number of frequency points rather than the size of each segments. if both
            are specified. Takes precedence over nperseg when both are specified.
        detrend : bool, optional
            remove DC and optionally linear trend, by default only removes DC. See
            scipy.signal.welch for more details.
        """
        signal = np.asanyarray(signal)
        if signal.ndim > 1:
            raise ValueError(
                f"got signal of shape {signal.shape}. Only one 1D signals are supported"
            )

        if nf is not None:
            nperseg = (nf - 1) * 2
        elif nperseg is None:
            nperseg = len(signal)

        if detrend is True:
            detrend = "constant"

        if window is None:
            window = "boxcar"

        freq, psd = sci_sig.welch(
            signal,
            fs=1 / dt,
            window=window,
            nperseg=nperseg,
            detrend=detrend,  # pyright: ignore
            scaling="density",
        )

        return cls(freq, psd)

    @property
    def fs(self) -> float:
        """sample frequency"""
        return self.freq[-1]

    @property
    def dt(self) -> float:
        """sample spacing"""
        return 0.5 / self.freq[-1]

    def plottable(
        self,
        dB: bool = True,
        wavelength: float | None = None,
        power: float | None = None,
        left: int | None = None,
        discard_nyquist: bool = True,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Transforms the PSD in a way that makes it easy to plot

        Parameters
        ----------
        dB : bool, optional
            transform the PSD from a linear scale to dB, by default True
        wavelength, power : float | None, optional
            if both are provided, will be used to compute the quantum noise limit and the PSD will
            be output relative to that amount
        left : int, optional
            Index of the first frequency point. The default is to drop only the 0 frequency
            point if it exits to simplify plotting in log-log scales. choose `left=0` to
            return everything
        discard_nyquist : bool, optional
            crop the psd before the Nyquist frequency, as this is a special point that is not
            guaranteed to be present and/or accurate depending on how the signal was generated, by
            default True

        Returns
        -------
        np.ndarray, shape (n,)
            frequency array
        np.ndarray, shape (n,)
            psd, with the desired transformation applied

        Example
        -------
        ```python
        noise = NoiseMeasurement(*np.load("my_measurement.npy"))
        plt.plot(*noise.plottable(wavelength=800e-9, power=0.3))  # dB above quantum limit
        plt.xscale("log")  # creates log-log plot since y is in dB by default
        plt.show()
        ```
        """
        psd = self.psd
        freq = self.freq
        if wavelength is not None and power is not None:
            psd = psd / quantum_noise_limit(wavelength, power)

        if dB:
            psd = to_dB(psd, ref=1.0)

        if freq.size % 2 and discard_nyquist:
            freq = freq[:-1]
            psd = psd[:-1]

        if left is None and freq[0] == 0:
            left = 1

        return freq[left:], psd[left:]

    def sample_spectrum(
        self, nf: int, dt: float | None = None, log_mode: bool = False, left: float | None = None
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        sample an amplitude spectrum with nt points. The corresponding sample spacing in the time
        is 1/freq.max().

        Parameters
        ----------
        nt : int
            number of points to sample
        dt : float | None, optional
            if given, freq will only be sampled up to 0.5/dt. if that value is higher than the
            max of freq, an exception is raised.
        left : float | None, optional
            extend current PSD to the lower frequency range by assuming a constant value of `left`.
            if None (default), extends with the last value
        log_mode : bool, optional
            sample on a log-log scale rather than on a linear scale, by default False
        """

        fmax = 0.5 / dt if dt is not None else self.freq.max()
        if fmax > self.freq.max():
            raise ValueError(
                f"{dt=} yields a max frequency of {fmax:g}Hz, but data only"
                f" goes up to {self.freq.max():g}Hz"
            )

        f = np.linspace(0, fmax, nf)
        if log_mode:
            interp = np.zeros_like(f)
            ind = self.freq > 0
            if left is not None and left <= 0:
                raise ValueError(f"value {left!r} for `left` in log mode is invalid")
            elif left is None:
                left: float = self.psd[ind][0]
            interp[1:] = np.exp(
                np.interp(
                    np.log(f[1:]),
                    np.log(self.freq[ind]),
                    np.log(self.psd[ind]),
                    left=np.log(left),
                    right=np.log(self.psd[ind][-1]),
                )
            )
            if self.freq[0] == 0:
                interp[0] = self.psd[0]
        else:
            left = left if left is not None else self.psd[0]
            interp = np.interp(f, self.freq, self.psd, left=left, right=self.psd[-1])
        return f, interp

    def resampled(
        self, nf: int, dt: float | None = None, log_mode: bool = False, left: float | None = None
    ) -> Self:
        return self.__class__(*self.sample_spectrum(nf, dt, log_mode, left))

    def time_series(
        self,
        nf: int | None = None,
        nt: int | None = None,
        dt: float | None = None,
        log_mode: bool = False,
        rng: np.random.Generator | int | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        computes a pulse train whose psd matches the measurement

        Parameters
        ----------
        nf : int | None, optional
            number of frequency points to sample. if None (default), will sample len(self.freq)
            Recommended is a power of 2 + 1 (129, 513, ...)
        nt : int | None, optional
            number of resulting time points. Ignored if nf is specified.
        dt : float | None, optional
            if given, choose a sample spacing of dt instead of 1/(2*f_max)
        log_mode : bool, optional
            sample on a log-log scale rather than on a linear scale, by default False

        Returns
        -------
        delays: np.ndarray

        """
        if nf is None and nt is None:
            if self._unif:
                nf = len(self.freq)
            else:
                raise ValueError(
                    "`nf` or `nt` must be specified when the frequency grid is not uniform"
                )
        elif nf is None:
            if nt % 2:
                raise ValueError(f"{nt=} is not even")
            else:
                nf = nt // 2 + 1

        if rng is None or isinstance(rng, (int, np.integer)):
            rng = np.random.default_rng(rng)

        freq, amp = self.sample_spectrum(nf, dt, log_mode, left=0)
        print(np.min(amp))
        fs = freq[-1] * 2

        if nf % 2:
            right = -1
            phase_n = nf - 2
        else:
            right = None
            phase_n = nf - 1

        amp[1:right] *= 0.5
        amp = np.sqrt(amp) + 0j
        amp[1:right] *= np.exp(2j * np.pi * rng.random(phase_n))
        signal = np.fft.irfft(amp) * np.sqrt((amp.size - 1) * 2 * fs)
        time = np.arange(len(signal)) / fs
        return time, signal

    def root_integrated(self, from_right: bool = True) -> np.ndarray:
        """
        returns the sqrt of the integrated spectrum
        The 0th component is the total RIN in the frequency range covered by the measurement
        Caution! this may be 0 frequency

        Parameters
        ----------
        from_right : bool, optional
            start integration at f[-1], by default True.
        """
        return integrated_noise(self.freq, self.psd, from_right)


def is_uniform(x: np.ndarray, rtol: float = 1e-10) -> bool:
    """
    Returns true if x is uniformly spaced from 0 to x_max
    within a coefficient of deviation of `rtol`

    Parameters
    ----------
    x : np.ndarray, shape (n,)
        *sorted* array
    rtol : float, optional
        relative tolerance, by default 1e-12
    """
    if x[0] != 0:
        return False
    diff = np.diff(x)
    return diff.std() / diff.mean() < rtol


def integrated_noise(freq: np.ndarray, psd: np.ndarray, from_right: bool = True) -> float:
    """
    given a normalized spectrum, computes the total rms RIN in the provided frequency window
    """
    s = slice(None, None, -1) if from_right else slice(None)
    return np.sqrt(
        cumulative_trapezoid(np.abs(psd)[s], (1 - 2 * from_right) * freq[s], initial=0)[s]
    )


def quantum_noise_limit(wavelength: float, power: float) -> float:
    return 2.0 * h * c / (power * wavelength)


def _validate_signal_input(
    spec: np.ndarray,
    w: np.ndarray,
    filters: Filters | None,
    peaks: float | np.ndarray | Sequence[float] | None,
    masks: np.ndarray | Sequence[float] | None,
):
    spec = np.atleast_2d(np.asarray(spec, dtype=complex))
    w = np.asarray(w, dtype=float)
    if spec.shape[-1] != w.shape[0]:
        raise ValueError(
            f"operands could not be broadcast together with shapes {spec.shape} {w.shape}"
        )
    if masks is not None:
        masks = np.asarray(masks, dtype=float)
        if masks.ndim != 2:
            raise TypeError("masks must be a 2D array")
        return spec, w, masks

    if filters is None:
        filters = Filters.empty()

    if peaks is None:
        peaks = [1.0] * len(filters)
    elif isinstance(peaks, (float, np.floating)):
        peaks = [peaks] * len(filters)
    elif isinstance(peaks, (np.ndarray, Sequence)) and len(peaks) == 1:
        peaks = [peaks[0]] * len(filters)
    elif isinstance(peaks, Sequence):
        peaks = np.array(peaks)
    else:
        raise TypeError(f"`peaks` of type {type(peaks)} invalid")

    masks = filters.generate(np.divide(TAUC, w, where=w != 0), peaks)
    return spec, w, masks


def energy_signal(
    spec: np.ndarray,
    w: np.ndarray,
    filters: Filters | None = None,
    peaks: float | list[float] | None = None,
    masks: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the energy signal resuling from bandpass filtering optical spectra.

    Parameters
    ----------
    spec : np.ndarray, shape (nt, nw)
        complex spectra
    w : np.ndarray, shape (nw,)
        angular frequency grid
    filters : Filters | None
        see Filters for more information, by default None, which means no filtering is done and only
        the total energy of each pulse is computed.
    peaks : float | list[float] | None, optional
        max **intensity** of each filter
    masks: np.ndarray, shape (m, nw,)
        raw mask array where 1.0 corresponds to no attenuation and 0.0 corresponds to complete
        absorbtion. values >1.0 or <0.0 are allowed but don't make sense physically.

    Returns
    -------
    energies : np.ndarray, shape(len(filters)+1, nt)
        energy of each pulse
    filtered_spectra : np.ndarray, shape(len(filters), nw)
        filtered spectra, including additional shot noise
    """
    spec, w, masks = _validate_signal_input(spec, w, filters, peaks, masks)
    return rs.noise_signal(spec, w, masks)


def jitter_signal(
    spec: np.ndarray,
    w: np.ndarray,
    filters: Filters | None = None,
    peaks: float | list[float] | None = None,
    masks: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the jitter signal resuling from bandpass filtering optical spectra.

    Parameters
    ----------
    spec : np.ndarray, shape (nt, nw)
        complex spectra
    w : np.ndarray, shape (nw,)
        angular frequency grid
    filters : Filters | None
        see Filters for more information, by default None, which means no filtering is done and only
        the total energy of each pulse is computed.
    peaks : float | list[float] | None, optional

    Returns
    -------
    energies : np.ndarray, shape(len(filters)+1, nt)
        energy of each pulse
    filtered_fields : np.ndarray, shape(len(filters), nw)
        filtered spectra, transformed back into electric field, including additional shot noise
    """
    return rs.jitter_signal(*_validate_signal_input(spec, w, filters, peaks, masks))
