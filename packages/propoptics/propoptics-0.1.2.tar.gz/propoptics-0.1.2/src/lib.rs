use core::str;
use numpy::{Complex64, IntoPyArray, PyArray1, PyArray2, PyReadonlyArray1, PyReadonlyArray2};
use std::{
    f64::{self, consts::PI},
    ops::Deref,
    sync::Arc,
};

use indicatif::ProgressBar;
use ndarray::parallel::prelude::*;
use ndarray::prelude::*;
use ndarray::Zip;
use physical_constants::REDUCED_PLANCK_CONSTANT as HBAR;
use pyo3::{exceptions::PyValueError, prelude::*};
use rand::prelude::*;
use rand_distr::StandardNormal;
use rustfft::{Fft, FftPlanner};

#[derive(Clone)]
enum IterMode {
    SinglePass,
    Product,
}

impl TryFrom<&str> for IterMode {
    type Error = PyErr;
    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value {
            "single_pass" => Ok(Self::SinglePass),
            "product" => Ok(Self::Product),
            _ => Err(PyErr::new::<PyValueError, _>("invalid iter_mode")),
        }
    }
}

impl<'py> FromPyObject<'py> for IterMode {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::PyAny>) -> PyResult<Self> {
        Self::try_from(ob.extract::<&str>()?)
    }
}

#[derive(Debug, Clone)]
enum ShotNoiseKind {
    VariablePhaseOnly,
    ConstantPhaseOnly,
    VariableBoth,
    ConstantBoth,
}

// impl TryFrom<Option<String>> for ShotNoiseKind {
impl<T> TryFrom<Option<T>> for ShotNoiseKind
where
    T: Deref<Target = str>,
{
    type Error = PyErr;
    fn try_from(value: Option<T>) -> Result<Self, Self::Error> {
        match value.as_deref() {
            None | Some("variable_phase_only") => Ok(Self::VariablePhaseOnly),
            Some("constant_phse_only") => Ok(Self::ConstantPhaseOnly),
            Some("variable_both") => Ok(Self::VariableBoth),
            Some("constant_both") => Ok(Self::ConstantBoth),
            _ => Err(PyErr::new::<PyValueError, _>("invalid shot noise kind")),
        }
    }
}

impl<'py> FromPyObject<'py> for ShotNoiseKind {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::PyAny>) -> PyResult<Self> {
        Self::try_from(ob.extract::<Option<String>>()?)
    }
}

enum SomeEnum {
    DefaultVariant,
    Variant2,
    Variant3,
}

impl<T> TryFrom<Option<T>> for SomeEnum
where
    T: Deref<Target = str>,
{
    type Error = PyErr;
    fn try_from(value: Option<T>) -> Result<Self, Self::Error> {
        match value.as_deref() {
            None | Some("variant_1") => Ok(Self::DefaultVariant),
            Some("variant_2") => Ok(Self::Variant2),
            Some("variant_3") => Ok(Self::Variant3),
            _ => Err(PyErr::new::<PyValueError, _>("Invalid value")),
        }
    }
}

impl<'py> FromPyObject<'py> for SomeEnum {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::PyAny>) -> PyResult<Self> {
        Self::try_from(ob.extract::<Option<String>>()?)
    }
}

#[derive(Debug, Clone)]
struct ShotNoise {
    kind: ShotNoiseKind,
    seed: Option<u64>,
}

impl ShotNoise {
    pub fn seed(&mut self, seed: Option<u64>) -> &mut Self {
        self.seed = seed;
        self
    }
    pub fn kind(&mut self, kind: ShotNoiseKind) -> &mut Self {
        self.kind = kind;
        self
    }

    pub fn gen(&self, w: ArrayView1<f64>) -> Array1<Complex64> {
        let dw = w[1] - w[0];
        let mut rng = match self.seed {
            Some(seed) => StdRng::seed_from_u64(seed),
            None => StdRng::from_os_rng(),
        };

        match self.kind {
            ShotNoiseKind::VariablePhaseOnly => w.mapv(move |val| sn_phase(val, dw, &mut rng)),
            ShotNoiseKind::ConstantPhaseOnly => w.mapv(move |_| sn_phase(w[0], dw, &mut rng)),
            ShotNoiseKind::VariableBoth => w.mapv(move |val| sn_both(val, dw, &mut rng)),
            ShotNoiseKind::ConstantBoth => w.mapv(move |_| sn_both(w[0], dw, &mut rng)),
        }
    }

    pub fn gen_default(w: ArrayView1<f64>) -> Array1<Complex64> {
        let mut rng = StdRng::from_os_rng();
        let dw = w[1] - w[0];
        w.mapv(move |val| sn_phase(val, dw, &mut rng))
    }
}

impl Default for ShotNoise {
    fn default() -> Self {
        ShotNoise {
            kind: ShotNoiseKind::VariablePhaseOnly,
            seed: None,
        }
    }
}

fn sn_both(value: f64, dw: f64, rng: &mut impl Rng) -> Complex64 {
    let std = f64::sqrt(0.5 * HBAR * (value.abs() / dw));
    Complex64::new(
        std * rng.sample::<f64, _>(StandardNormal),
        std * rng.sample::<f64, _>(StandardNormal),
    )
}

fn sn_phase(value: f64, dw: f64, rng: &mut StdRng) -> Complex64 {
    let phase = 2.0 * PI * rng.random::<f64>();
    let std = f64::sqrt(0.5 * HBAR * (value.abs() / dw));
    Complex64::new(std, 0.0) * Complex64::new(0.0, phase).exp()
}

/// Attenuates a complex spectrum while taking into consideration shot noise
/// a new shot noise spectrum is generated and apply proportionnally to the attenuation
///
/// # Arguments
///
/// * `values` - values to mask
/// * `mask` - mask to apply. Should be already normalized such that the peak is at sqrt(true_peak)
/// * `w` - angular frequency grid (to generate shot noise)
fn mask_norm_noise(
    spectra: ArrayView1<Complex64>,
    mask: ArrayView1<f64>,
    w: ArrayView1<f64>,
) -> f64 {
    let noise = ShotNoise::gen_default(w);
    let dw = w[1] - w[0];
    spectra
        .iter()
        .zip(mask.iter())
        .zip(noise.iter())
        .fold(0.0, |acc, ((val, ma), no)| {
            let newval = val * ma + no * f64::sqrt(1.0 - ma.powi(2));
            acc + dw * newval.norm_sqr()
        })
}

/// Attenuates a complex spectrum while taking into consideration shot noise
/// a new shot noise spectrum is generated and apply proportionnally to the attenuation
///
/// # Arguments
///
/// * `values` - values to mask
/// * `mask` - mask to apply. Should be already normalized such that the peak is at sqrt(true_peak)
/// * `w` - angular frequency grid (to generate shot noise)
fn mask_center_of_gravity_noise(
    spectra: ArrayView1<Complex64>,
    mask: ArrayView1<f64>,
    w: ArrayView1<f64>,
    dt: f64,
    fft: Arc<dyn Fft<f64>>,
) -> f64 {
    let noise = ShotNoise::gen_default(w);
    let mut newvals = Zip::from(&spectra)
        .and(&mask)
        .and(&noise)
        .map_collect(|&s, &m, &n| s * m + n * f64::sqrt(1.0 - m.powi(2)));
    fft.process(newvals.as_slice_mut().unwrap());
    _center_of_gravity(newvals.view(), dt)
}

fn mask_noise(
    values: ArrayView1<Complex64>,
    mask: ArrayView1<f64>,
    w: ArrayView1<f64>,
) -> Array1<Complex64> {
    let noise = ShotNoise::gen_default(w);
    Zip::from(&noise)
        .and(&values)
        .and(&mask)
        .map_collect(|no, val, ma| val * ma + *no * f64::sqrt(1.0 - ma.powi(2)))
}

fn norm(spectra: ArrayView1<Complex64>, dx: f64) -> f64 {
    spectra.fold(0.0, move |acc, v| acc + dx * v.norm_sqr())
}

fn center_of_gravity(spectra: ArrayView1<Complex64>, dt: f64, fft: Arc<dyn Fft<f64>>) -> f64 {
    let mut fields = spectra.to_owned();
    fft.process(fields.as_slice_mut().unwrap());
    _center_of_gravity(fields.view(), dt)
}

fn _center_of_gravity(values: ArrayView1<Complex64>, dt: f64) -> f64 {
    let new_vals = values.mapv(|v| v.norm_sqr());
    let offset = 0.5 * (values.len() as f64) * dt;
    new_vals
        .iter()
        .enumerate()
        .fold(0.0, |acc, (i, v)| acc + ((i as f64) * dt - offset) * v)
        / new_vals.sum()
}

/// Reduces Axis(1) of mat by applying reduc_fn over it
///
/// # Arguments
///
/// * `out` - where to place the input. 1d slice of same length as Axis(0) of mat
/// * `mat` - t
/// * `reduc_fn` - function that reduces one single spectrum into one number
fn complex_reduce_inplace<F>(out: &mut [f64], mat: ArrayView2<Complex64>, reduc_fn: F)
where
    F: Fn(ArrayView1<Complex64>) -> f64 + Sync,
{
    mat.axis_iter(Axis(0))
        .into_par_iter()
        .zip(out)
        .for_each(|(val, o)| *o = reduc_fn(val));
}

fn energy_signals(
    spectra: ArrayView2<Complex64>,
    w: ArrayView1<f64>,
    masks: ArrayView2<f64>,
) -> (Array2<f64>, Array2<Complex64>) {
    let mut out = Array2::zeros((masks.shape()[0] + 1, spectra.dim().0));
    complex_reduce_inplace(
        out.slice_mut(s![0, ..])
            .as_slice_mut()
            .expect("new array should be aligned"),
        spectra,
        |row| norm(row, w[1] - w[0]),
    );
    let first_spectrum = spectra.slice(s![0, ..]);
    let pg = if masks.shape()[0] > 1 {
        ProgressBar::new(masks.shape()[0] as u64)
    } else {
        ProgressBar::hidden()
    };
    let mut filtered_spectra = Array2::zeros((masks.shape()[0], w.len()));
    for (i, mask) in masks.outer_iter().enumerate() {
        filtered_spectra.slice_mut(s![i, ..]).assign(&mask_noise(
            first_spectrum.view(),
            mask.view(),
            w.view(),
        ));
        complex_reduce_inplace(
            out.slice_mut(s![i + 1, ..])
                .as_slice_mut()
                .expect("brand new array should be aligned"),
            spectra,
            move |val| mask_norm_noise(val, mask.view(), w),
        );
        pg.inc(1);
    }
    pg.finish();
    (out, filtered_spectra)
}

fn jitter_signals(
    spectra: ArrayView2<Complex64>,
    w: ArrayView1<f64>,
    masks: ArrayView2<f64>,
) -> (Array2<f64>, Array2<Complex64>) {
    let mut out = Array2::zeros((masks.shape()[0] + 1, spectra.dim().0));
    let mut planner = FftPlanner::<f64>::new();
    let ifft = planner.plan_fft_inverse(spectra.dim().1);
    let dt = ((w[1] - w[0]) * 0.5 / PI * (w.len() as f64)).recip();
    let first_spectrum = spectra.slice(s![0, ..]);
    let pg = if masks.shape()[0] > 1 {
        ProgressBar::new(masks.shape()[0] as u64)
    } else {
        ProgressBar::hidden()
    };
    pg.set_prefix("jitter");

    complex_reduce_inplace(
        out.slice_mut(s![0, ..])
            .as_slice_mut()
            .expect("new array should be aligned"),
        spectra,
        |row| center_of_gravity(row, dt, ifft.clone()),
    );

    let mut filtered_fields = Array2::zeros((masks.shape()[0], w.len()));
    for (i, mask) in masks.outer_iter().enumerate() {
        filtered_fields.slice_mut(s![i, ..]).assign(&mask_noise(
            first_spectrum.view(),
            mask.view(),
            w,
        ));
        ifft.process(filtered_fields.slice_mut(s![i, ..]).as_slice_mut().unwrap());
        complex_reduce_inplace(
            out.slice_mut(s![i + 1, ..])
                .as_slice_mut()
                .expect("brand new array should be aligned"),
            spectra,
            |val| mask_center_of_gravity_noise(val, mask.view(), w, dt, ifft.clone()),
        );
        pg.inc(1);
    }
    pg.finish();
    (out, filtered_fields)
}

#[pyfunction]
#[pyo3(name = "noise_signal")]
fn py_energy_signal<'py>(
    py: Python<'py>,
    spectra: PyReadonlyArray2<Complex64>,
    w: PyReadonlyArray1<f64>,
    masks: PyReadonlyArray2<f64>,
) -> (Bound<'py, PyArray2<f64>>, Bound<'py, PyArray2<Complex64>>) {
    let (signal, spectra) = energy_signals(spectra.as_array(), w.as_array(), masks.as_array());
    (signal.into_pyarray(py), spectra.into_pyarray(py))
}
#[pyfunction]
#[pyo3(name = "jitter_signal")]
fn py_jitter_signal<'py>(
    py: Python<'py>,
    spectra: PyReadonlyArray2<Complex64>,
    w: PyReadonlyArray1<f64>,
    masks: PyReadonlyArray2<f64>,
) -> (Bound<'py, PyArray2<f64>>, Bound<'py, PyArray2<Complex64>>) {
    let (signal, spectra) = jitter_signals(spectra.as_array(), w.as_array(), masks.as_array());
    (signal.into_pyarray(py), spectra.into_pyarray(py))
}
#[pyfunction]
#[pyo3(name = "shot_noise")]
fn py_shot_noise<'py>(
    py: Python<'py>,
    w: PyReadonlyArray1<f64>,
    kind: ShotNoiseKind,
    seed: Option<u64>,
) -> Bound<'py, PyArray1<Complex64>> {
    ShotNoise::default()
        .kind(kind)
        .seed(seed)
        .gen(w.as_array().view())
        .into_pyarray(py)
}

#[pyfunction]
#[pyo3(name = "mask_noise")]
fn py_mask_noise<'py>(
    py: Python<'py>,
    w: PyReadonlyArray1<f64>,
    spectrum: PyReadonlyArray1<Complex64>,
    mask: PyReadonlyArray1<f64>,
) -> Bound<'py, PyArray1<Complex64>> {
    mask_noise(
        spectrum.as_array().view(),
        mask.as_array().view(),
        w.as_array().view(),
    )
    .into_pyarray(py)
}

#[pymodule]
#[pyo3(name = "_lib_propoptics")]
fn scgrs(_: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_energy_signal, m)?)?;
    m.add_function(wrap_pyfunction!(py_jitter_signal, m)?)?;
    m.add_function(wrap_pyfunction!(py_shot_noise, m)?)?;
    m.add_function(wrap_pyfunction!(py_mask_noise, m)?)?;

    Ok(())
}
