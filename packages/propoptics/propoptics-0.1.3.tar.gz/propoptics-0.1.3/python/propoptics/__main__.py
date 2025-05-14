import importlib.metadata
import random
import sys
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Sequence

import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import typer

import propoptics as po
from propoptics.interface import auto_read_2d_file

__version__ = importlib.metadata.version("propoptics")
del importlib.metadata

app = typer.Typer(no_args_is_help=True)


class Scale(StrEnum):
    LINEAR = "linear"
    DBM = "dBm"
    DBC = "dBc"


PSDFILE_T = Annotated[
    Path,
    typer.Argument(
        help="Path to the PSD measurement file. "
        "The data must be represented with positive frequency only, i.e. negative and positive "
        "frequency contributions already added together."
    ),
]
REF_T = Annotated[
    float | None,
    typer.Option(help="for dBm `scale` only. Reference voltage, i.e. DC voltage in V."),
]
IMPEDANCE_T = Annotated[
    float,
    typer.Option(help="for dBm `scale` only. impedance of the signal chain in Ohm"),
]
POWER_T = Annotated[
    float | None,
    typer.Option(help="Long term mean power (in W) for shot-noise limit calculations."),
]
WAVELENGTH_T = Annotated[
    float | None,
    typer.Option(help="Center wavelength (in m) for shot-noise limit calculations."),
]
SCALE_T = Annotated[Scale, typer.Option(case_sensitive=False)]


def version_callback(version: bool = False) -> None:
    if version:
        print(f"propoptics {__version__}")
        sys.exit(0)  # typer.Exit() does not quit immediately


VERSION_T = Annotated[
    bool,
    typer.Option(
        "--version",
        "-v",
        help="Show propoptics version (on stdout) and quit.",
        show_default=False,
        is_eager=True,
        callback=version_callback,
    ),
]


def get_noise_measurement(
    psd_file: Path,
    scale: Scale = Scale.LINEAR,
    ref: float = None,
    impedance: float = 50.0,
    power: float | None = None,
    wavelength: float | None = None,
) -> tuple[po.NoiseMeasurement, po.NoiseMeasurement | None]:
    if not psd_file.exists():
        raise FileNotFoundError(f"file {psd_file} not found")
    x, y = auto_read_2d_file(psd_file)
    if scale is Scale.LINEAR:
        noise = po.NoiseMeasurement(x, y)
    elif scale is Scale.DBC:
        noise = po.NoiseMeasurement.from_dBc(x, y)
    elif scale is Scale.DBM:
        if ref is None:
            raise ValueError("`--ref` must be specified when using dBm. Use `--help` for more info")
        noise = po.NoiseMeasurement.from_dBm(x, y, ref, impedance)
    if wavelength is not None and power is not None:
        qn_limit = po.quantum_noise_limit(wavelength, power)
        adjusted_noise = po.NoiseMeasurement(noise.freq, np.maximum(noise.psd - qn_limit, 0.0))
    else:
        adjusted_noise = None
    return noise, adjusted_noise


def write_data(data: Sequence[np.ndarray], labels: Sequence[str] | None, output_path: Path | None):
    if labels is not None and len(labels) != len(data):
        raise ValueError("`labels`, when given, must have the same length as `data`")
    if labels is None:
        labels = (f"arr{i:02d}" for i in range(len(data)))

    if output_path is None:
        np.savetxt(
            sys.stdout,
            np.c_[*data],
            fmt="%.16g",
            delimiter=",",
            header=",".join(labels),
        )
        return

    suffix = output_path.suffix.lower()
    if suffix == ".npy":
        np.save(output_path, data)
    elif suffix == ".mat":
        scipy.io.savemat(output_path, {k: v for k, v in zip(labels, data)}, oned_as="column")
    elif suffix == ".npz":
        np.savez(output_path, **{k: v for k, v in zip(labels, data)})
    else:
        delimiter = {".csv": ",", ".tsv": "\t", ".txt": " ", ".dat": " "}[suffix]
        np.savetxt(
            output_path,
            np.c_[*data],
            fmt="%.16g",
            delimiter=delimiter,
            header=delimiter.join(labels),
        )


@app.callback()
def common(
    version: VERSION_T = False,
):
    pass


@app.command(
    help="open a noise measurement file and plot it in order to check that import settings"
)
def check(
    psd_file: Path,
    scale: SCALE_T = Scale.LINEAR,
    ref: REF_T = None,
    impedance: IMPEDANCE_T = 50.0,
    power: POWER_T = None,
    wavelength: WAVELENGTH_T = None,
    version: VERSION_T = False,
):
    try:
        noise, adjusted_noise = get_noise_measurement(
            psd_file, scale, ref, impedance, power, wavelength
        )
    except Exception as e:
        typer.echo(e, err=True)
        return

    plt.xscale("log")
    plt.xlabel("Hz")
    plt.ylabel("dBc/Hz")
    plt.title(psd_file)
    plt.plot(*noise.plottable(), label="raw measurement")

    if adjusted_noise is not None:
        qn_limit_db = 10 * np.log10(po.quantum_noise_limit(wavelength, power))
        qn_label = f"Computed shot-noise limit of {qn_limit_db:.2f} dBc/Hz"
        plt.plot(*adjusted_noise.plottable(), label="SN-adjusted")
        plt.text(0.5, 0.98, qn_label, transform=plt.gca().transAxes, ha="center", va="top")
        plt.legend()

    plt.tight_layout()
    plt.show()


@app.command(
    help="Generate a pulse train from a noise measurement file. When `power` and `wavelength` are "
    "specified, the shot-noise limit is calculated and a second time series where it is "
    "substracted is generated. Using this adjusted time series on pulses where shot noise is added "
    "in the optical domain will result in the original noise PSD."
)
def time_series(
    psd_file: PSDFILE_T,
    scale: SCALE_T = Scale.LINEAR,
    ref: REF_T = None,
    impedance: IMPEDANCE_T = 50.0,
    power: POWER_T = None,
    wavelength: WAVELENGTH_T = None,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="output path. Data format is deduced from file extension. When no output path is "
            "given, the data is printed to the stdout in csv format",
            resolve_path=True,
        ),
    ] = None,
    nf: Annotated[
        int | None,
        typer.Option(
            help="number of frequency points to sample. Recommended is 2^n+1, i.e. 257, 513, ..."
        ),
    ] = None,
    nt: Annotated[
        int | None,
        typer.Option(
            help="number of temporal points to sample. Takes precedence over `nf`. "
            "Recommended is a power of 2."
        ),
    ] = None,
    dt: Annotated[float | None, typer.Option()] = None,
    log_mode: Annotated[
        bool,
        typer.Option("--log", help="interpolate the PSD on a log scale instead of linear scale"),
    ] = False,
    noise_seed: Annotated[
        int | None, typer.Option(help="set the noise seed of the random phase for reproducibility")
    ] = None,
    plot: Annotated[bool, typer.Option("--plot", help="plot the pulse train")] = False,
    version: VERSION_T = False,
):
    try:
        noise, adjusted_noise = get_noise_measurement(
            psd_file, scale, ref, impedance, power, wavelength
        )
    except Exception as e:
        typer.echo(e, err=True)
        return

    adjusted_signal = None

    if noise_seed is None:
        noise_seed = random.randint(0, 1 << 32)

    if noise is None:
        return
    try:
        time, signal = noise.time_series(nf, nt, dt, log_mode, noise_seed)
    except Exception as e:
        typer.echo(e, err=True)
        return
    if adjusted_noise is not None:
        try:
            _, adjusted_signal = adjusted_noise.time_series(nf, nt, dt, log_mode, noise_seed)
        except Exception as e:
            typer.echo(e, err=True)
            return
    data = [time, signal]
    labels = ["time", "raw signal"]
    if adjusted_signal is not None:
        data.append(adjusted_signal)
        labels.append("SN-substracted signal")

    try:
        write_data(data, labels, output)
    except Exception as e:
        typer.echo(e, err=True)
        return

    if plot:
        if output is not None:
            plt.title(output)
        for data, label in zip(data[1:], labels[1:]):
            plt.plot(time, data, marker=".", ls="", label=label)
        plt.xlabel("time (s)")
        plt.ylabel("deviation from mean (%)")
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app()
