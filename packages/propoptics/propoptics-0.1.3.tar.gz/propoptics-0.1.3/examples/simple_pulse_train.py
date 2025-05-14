from pathlib import Path

import matplotlib.pyplot as plt
import propoptics as po
import numpy as np


def main():
    # load the measurement
    freq, rin_psd = np.load(Path(__file__).parent / "rin_psd.npy")
    # measurement is in linear scale (1/Hz). Use NoiseMeasurement.from_dBc to load data in dBc/Hz
    rin_obj = po.NoiseMeasurement(freq, rin_psd)
    # generate a signal. Setting `rng` makes it reproducible
    t, signal = rin_obj.time_series(nt=32, rng=123456789)

    plt.plot(1e6 * t, 1e2 * signal, "o")
    plt.xlabel("time (μs)")
    plt.ylabel("% deviation")
    plt.axhline(0, c="0.8")
    plt.show()


if __name__ == "__main__":
    main()
