use std::fmt;

use pyo3::{exceptions::PyValueError, prelude::*};

use symbologyl2::us::equities as us_equities;

#[derive(Debug)]
struct PySymbologyError {
    pub msg: String,
}

impl std::error::Error for PySymbologyError {}

impl fmt::Display for PySymbologyError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.msg)
    }
}

impl std::convert::From<PySymbologyError> for PyErr {
    fn from(err: PySymbologyError) -> PyErr {
        PyValueError::new_err(err.to_string())
    }
}

impl std::convert::From<us_equities::SymbologyError> for PySymbologyError {
    fn from(err: us_equities::SymbologyError) -> Self {
        PySymbologyError {
            msg: err.to_string(),
        }
    }
}

#[pyfunction]
fn from_any_to_root(symbol: String) -> Result<String, PySymbologyError> {
    let res = us_equities::parse(&symbol).map_err(PySymbologyError::from)?;
    Ok(String::from(res.root().as_str()))
}

#[pyfunction]
fn from_any_to_cms(symbol: String) -> Result<String, PySymbologyError> {
    us_equities::from_any_to_cms(&symbol).map_err(PySymbologyError::from)
}

#[pyfunction]
fn from_any_to_cqs(symbol: String) -> Result<String, PySymbologyError> {
    us_equities::from_any_to_cqs(&symbol).map_err(PySymbologyError::from)
}

#[pyfunction]
fn from_any_to_nasdaq_integrated(symbol: String) -> Result<String, PySymbologyError> {
    us_equities::from_any_to_nasdaq(&symbol).map_err(PySymbologyError::from)
}

macro_rules! get_suffix {
    ($func_name:ident, $getter:ident) => {
        #[pyfunction]
        fn $func_name(symbol: String) -> Result<Option<String>, PySymbologyError> {
            let res = us_equities::parse(&symbol).map_err(PySymbologyError::from)?;
            if let Some(suffix) = res.suffix() {
                suffix
                    .$getter()
                    .map_err(PySymbologyError::from)
                    .map(|x| Some(String::from(x.as_str())))
            } else {
                Ok(None)
            }
        }
    };
}

get_suffix!(from_any_to_cms_suffix, cms_suffix);
get_suffix!(from_any_to_cqs_suffix, cqs_suffix);
get_suffix!(from_any_to_nasdaq_suffix, nasdaq_integrated_suffix);

#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(from_any_to_root, m)?)?;
    m.add_function(wrap_pyfunction!(from_any_to_cms, m)?)?;
    m.add_function(wrap_pyfunction!(from_any_to_cqs, m)?)?;
    m.add_function(wrap_pyfunction!(from_any_to_nasdaq_integrated, m)?)?;
    m.add_function(wrap_pyfunction!(from_any_to_cms_suffix, m)?)?;
    m.add_function(wrap_pyfunction!(from_any_to_cqs_suffix, m)?)?;
    m.add_function(wrap_pyfunction!(from_any_to_nasdaq_suffix, m)?)?;
    Ok(())
}
