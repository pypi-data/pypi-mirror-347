//! Python bindings for eBIRForms window automation.

pub mod automation_utils;
pub mod constants;
mod window_utils;
pub mod workflows;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use uiautomation::UIAutomation;
use uiautomation::types::Handle;

/// Error conversion helper function to convert workflow errors to Python exceptions
fn convert_error(error: workflows::WorkflowError) -> PyErr {
    match error {
        workflows::WorkflowError::UIAutomation(e) => {
            PyRuntimeError::new_err(format!("UIAutomation error: {:?}", e))
        }
        workflows::WorkflowError::WindowNotFound => PyRuntimeError::new_err(
            "eBIRForms window not found. Please call open_ebir_window first.",
        ),
        workflows::WorkflowError::ElementNotFound(e) => {
            PyRuntimeError::new_err(format!("Element not found: {}", e))
        }
        workflows::WorkflowError::Timeout(e) => {
            PyRuntimeError::new_err(format!("Timeout waiting for element: {}", e))
        }
        workflows::WorkflowError::Other(e) => PyRuntimeError::new_err(format!("Error: {}", e)),
    }
}

#[pyfunction]
/// Launch or focus the eBIRForms application and arrange the window for automation.
/// This is the Python-exposed entry point.
fn auto_open_ebir_window(use_winapi: Option<bool>, ebir_path: Option<&str>) -> PyResult<usize> {
    let use_winapi = use_winapi.unwrap_or(true);
    match crate::window_utils::open_ebir_window(Some(use_winapi), ebir_path) {
        Some(hwnd) => Ok(hwnd.0 as usize),
        None => Err(PyRuntimeError::new_err(
            "Failed to open or find eBIRForms window.",
        )),
    }
}

/// represents eBIRFormsAutomation class
#[pyclass]
pub struct EBirformsAutomation {
    hwnd: usize, // Store HWND as usize for Python compatibility
}

impl EBirformsAutomation {
    fn get_uia_and_root(&self) -> PyResult<(UIAutomation, uiautomation::UIElement)> {
        let uia = UIAutomation::new().map_err(|e| {
            PyRuntimeError::new_err(format!("Failed to initialize UI Automation: {:?}", e))
        })?;
        let handle = Handle::from(self.hwnd as isize);
        let root = uia
            .element_from_handle(handle)
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to get root element: {:?}", e)))?;
        Ok((uia, root))
    }
}

#[pymethods]
impl EBirformsAutomation {
    #[new]
    fn new(hwnd: usize) -> Self {
        Self { hwnd }
    }
    fn type_tin(&self, tin1: &str, tin2: &str, tin3: &str, tin4: &str) -> PyResult<()> {
        let (uia, root_element) = self.get_uia_and_root()?;
        if let Err(e) = crate::workflows::type_tin(tin1, tin2, tin3, tin4, &uia, &root_element) {
            Err(convert_error(e))
        } else {
            Ok(())
        }
    }
    fn select_form(&self, form: &str, fill_up: bool) -> PyResult<bool> {
        let (uia, root_element) = self.get_uia_and_root()?;
        match crate::workflows::select_form(form, fill_up, &uia, &root_element) {
            Ok(result) => Ok(result),
            Err(e) => Err(convert_error(e)),
        }
    }
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn ebir_automation(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(auto_open_ebir_window, m)?)?;
    m.add_class::<EBirformsAutomation>()?;

    Ok(())
}
