import numpy as np
from pathlib import Path
from io import BytesIO


def _read_npy(data: bytes) -> np.array:
    arr = np.load(BytesIO(data))
    if arr.ndim != 2:
        raise ValueError()
    if arr.shape[0] != 2 and arr.shape[1] == 2:
        arr = arr.T
    return arr


def _decode_csv(s: str) -> np.ndarray:
    lines = s.splitlines()
    for delim in (",", "\t", "|", " "):
        try:
            arr = np.loadtxt(lines, delimiter=delim)
            break
        except Exception:
            continue
    else:
        raise ValueError()
    return arr


def _read_csv(data: bytes) -> np.array:
    text = data.decode()
    try:
        return _decode_csv(text)
    except Exception:
        pass
    return _decode_csv(text.replace(",", "."))


def auto_read_2d_file(path: Path, y_col: int = 1) -> tuple[np.ndarray, np.ndarray]:
    """Tries to open a file containing float data and return a x and y array

    Parameters
    ----------
    path : Path
        path to the file
    y_col : int
        if the path contains more than 2 columns, tells which one to
        use of the y values, by default 1

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        x and y arrays

    """

    if not path.exists():
        raise FileNotFoundError
    data = path.read_bytes()
    for func in (_read_npy, _read_csv):
        try:
            arr = func(data)
            break
        except Exception:
            continue
    else:
        raise ValueError(f"Could not interpret data in '{path}'")
    return arr[0], arr[y_col]
