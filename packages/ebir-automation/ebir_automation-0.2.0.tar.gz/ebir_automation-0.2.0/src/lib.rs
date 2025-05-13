//! Python bindings for eBIRForms window automation.

mod window_utils;
use pyo3::prelude::*;

#[pyfunction]
/// Launch or focus the eBIRForms application and arrange the window for automation.
/// This is the Python-exposed entry point.
fn open_ebir_window_py(use_winapi: Option<bool>, ebir_path: Option<&str>) -> PyResult<()> {
    let use_winapi = use_winapi.unwrap_or(true);
    crate::window_utils::open_ebir_window(Some(use_winapi), ebir_path);
    Ok(())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn ebir_automation(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(open_ebir_window_py, m)?)?;

    Ok(())
}
