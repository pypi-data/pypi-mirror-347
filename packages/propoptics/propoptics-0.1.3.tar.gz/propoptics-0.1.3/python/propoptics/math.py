from typing import TypeVar
import warnings

import numpy as np

T = TypeVar("T", float, complex, np.floating, np.ndarray)


def abs2(x: T) -> T:
    return x.real**2 + x.imag**2


def to_dB(arr: np.ndarray, ref=None, axis=None, avoid_nan: bool = False) -> np.ndarray:
    """
    converts unitless values in dB

    Parameters
    ----------
    arr : np.ndarray
        array of non-negative values. Any values 0 or below will be mapped to the minimum
        positive value in dB
    ref : float, optional
        reference value corresponding to 0dB (default : max(arr))
    axis : int | None, optional
        on which axis to apply the transformation. If `ref` is given, this has no effect

    Returns
    ----------
    np.ndarray
        array in dB
    """
    if axis is not None and arr.ndim > 1 and ref is None:
        return np.apply_along_axis(to_dB, axis, arr)

    if ref is None:
        ref = np.max(arr)
    above_0 = arr > 0
    if not np.any(above_0) or ref <= 0:
        raise ValueError("invalid array to convert to dB")
    m = arr / ref
    if avoid_nan:
        out = np.ones_like(arr) * (10 * np.log10(m[above_0].min()))
    else:
        out = np.empty_like(arr)
        out[:] = np.nan
    return 10 * np.log10(m, out=out, where=above_0)
