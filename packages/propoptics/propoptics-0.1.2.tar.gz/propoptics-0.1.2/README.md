# Propoptics

`propoptics` is a small Python library aimed at providing tools to generate pulse train based on measured noise power spectral densities (PSDs), as done in \[1\]. Moreover, it provides a limited number of analysis tools:

- Tooling for spectral filtering and integration, allowing users to quickly convert a series of optical spectra into a sequence of values (energy or timing delay).
- A wrapper around `scipy.signal.welch` to make power spectral density estimations easier.

Supported diagnostics are:

| Time series data | Frequency data           |
| ---------------- | ------------------------ |
| energy           | relative intensity noise |
| timing delay           | timing jitter, directly related to phase noise |


# Installation

## Run using `uv tool`

The easiest way to use the command-line interface (CLI) is to [install `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)

You can use `propoptics` in your own project by simply installing the package from PyPI. 
```
pip install propoptics
```

The minimum supported Python version is 3.11.

You can also install from source, in which case you must install the development dependencies and have a [Rust](https://www.rust-lang.org/tools/install) compiler installed. `rustc 1.86.0` is the only version tested.

```
pip install -r requirements_dev.txt 
maturin develop

# run tests
cargo test
pytest
```

# Quick start

Generate a pulse train:

```python
import propoptics
import numpy as np

freq, rin_psd = np.load("path/to/measurement")
rin_obj = propoptics.NoiseMeasurement(freq, rin_psd)
t, signal = rin_obj.time_series(nt=32, rng=123456789)
```

Complete example in `./examples/simple_pulse_train.py`.

# Welch method
The total number of points must account for 50% overlap when using the Welch method

Each · corresponds to one pulse:
```
 time -->
 0             nt/2              nt
 ┃·······┃·······┃·······┃·······┃
 ┆   ┃·······┃·······┃·······┃
 ┆   ┆               ┆       ┆
 ┆   ┆              >┆       ┆< = nperseg
>┆   ┆< = nperseg // 2
```

# Reference

\[1\] CAMENZIND, Sandro L., SIERRO, Benoît, WILLENBERG, Benjamin, et al. Ultra-low noise spectral broadening of two combs in a single ANDi fiber. APL Photonics, 2025, vol. 10, no 3.
