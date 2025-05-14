//! Python bindings for eBIRForms window automation.

pub mod automation_utils;
pub mod constants;
mod window_utils;
pub mod workflows;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;

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
fn open_ebir_window_py(use_winapi: Option<bool>, ebir_path: Option<&str>) -> PyResult<()> {
    let use_winapi = use_winapi.unwrap_or(true);
    crate::window_utils::open_ebir_window(Some(use_winapi), ebir_path);
    Ok(())
}

/// Type a TIN (Tax Identification Number) into the form fields.
/// This is a Python-exposed function that automates filling in TIN fields.
#[pyfunction]
fn type_tin_py(tin1: &str, tin2: &str, tin3: &str, tin4: &str) -> PyResult<()> {
    // Get the window handle from window_utils
    if let Some(hwnd) = crate::window_utils::get_ebir_window() {
        crate::workflows::type_tin(tin1, tin2, tin3, tin4, hwnd);
        Ok(())
    } else {
        Err(PyRuntimeError::new_err(
            "eBIRForms window not found. Please call open_ebir_window first.",
        ))
    }
}

/// Navigate to a section in the eBIRForms application.
/// This is a Python-exposed function that automates navigating to a specific section.
#[pyfunction]
fn navigate_to_section_py(section_name: &str) -> PyResult<()> {
    // Get the window handle from window_utils
    if let Some(hwnd) = crate::window_utils::get_ebir_window() {
        crate::workflows::navigate_to_section(section_name, hwnd).map_err(convert_error)
    } else {
        Err(PyRuntimeError::new_err(
            "eBIRForms window not found. Please call open_ebir_window first.",
        ))
    }
}

/// Click a button in the eBIRForms application.
/// This is a Python-exposed function that automates clicking a button by name.
#[pyfunction]
fn click_button_py(button_name: &str) -> PyResult<()> {
    // Get the window handle from window_utils
    if let Some(hwnd) = crate::window_utils::get_ebir_window() {
        crate::workflows::click_button(button_name, hwnd).map_err(convert_error)
    } else {
        Err(PyRuntimeError::new_err(
            "eBIRForms window not found. Please call open_ebir_window first.",
        ))
    }
}

/// Select a tax type from the dropdown.
/// This is a Python-exposed function that automates selecting a tax type.
#[pyfunction]
fn select_tax_type_py(tax_type: &str) -> PyResult<()> {
    // Get the window handle from window_utils
    if let Some(hwnd) = crate::window_utils::get_ebir_window() {
        crate::workflows::select_tax_type(tax_type, hwnd).map_err(convert_error)
    } else {
        Err(PyRuntimeError::new_err(
            "eBIRForms window not found. Please call open_ebir_window first.",
        ))
    }
}

/// Check or uncheck the accept terms checkbox.
/// This is a Python-exposed function that automates checking or unchecking the accept terms.
#[pyfunction]
fn set_accept_terms_py(check: bool) -> PyResult<()> {
    // Get the window handle from window_utils
    if let Some(hwnd) = crate::window_utils::get_ebir_window() {
        crate::workflows::set_accept_terms(check, hwnd).map_err(convert_error)
    } else {
        Err(PyRuntimeError::new_err(
            "eBIRForms window not found. Please call open_ebir_window first.",
        ))
    }
}

/// Complete the form workflow from start to submission.
/// This is a Python-exposed function that automates the entire form fill and submission process.
#[pyfunction]
fn complete_form_py(
    tin1: &str,
    tin2: &str,
    tin3: &str,
    tin4: &str,
    tax_type: &str,
) -> PyResult<()> {
    // Get the window handle from window_utils
    if let Some(hwnd) = crate::window_utils::get_ebir_window() {
        crate::workflows::complete_form(tin1, tin2, tin3, tin4, tax_type, hwnd)
            .map_err(convert_error)
    } else {
        Err(PyRuntimeError::new_err(
            "eBIRForms window not found. Please call open_ebir_window first.",
        ))
    }
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn ebir_automation(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(open_ebir_window_py, m)?)?;
    m.add_function(wrap_pyfunction!(type_tin_py, m)?)?;
    m.add_function(wrap_pyfunction!(navigate_to_section_py, m)?)?;
    m.add_function(wrap_pyfunction!(click_button_py, m)?)?;
    m.add_function(wrap_pyfunction!(select_tax_type_py, m)?)?;
    m.add_function(wrap_pyfunction!(set_accept_terms_py, m)?)?;
    m.add_function(wrap_pyfunction!(complete_form_py, m)?)?;

    // Add module-level constants for sections
    m.add("SECTION_TAXPAYER_INFO", constants::SECTION_TAXPAYER_INFO)?;
    m.add("SECTION_TAX_TYPE", constants::SECTION_TAX_TYPE)?;
    m.add(
        "SECTION_PAYMENT_DETAILS",
        constants::SECTION_PAYMENT_DETAILS,
    )?;
    m.add("SECTION_SUMMARY", constants::SECTION_SUMMARY)?;

    // Add module-level constants for buttons
    m.add("BUTTON_NEXT", constants::BUTTON_NEXT)?;
    m.add("BUTTON_PREVIOUS", constants::BUTTON_PREVIOUS)?;
    m.add("BUTTON_SUBMIT", constants::BUTTON_SUBMIT)?;
    m.add("BUTTON_CANCEL", constants::BUTTON_CANCEL)?;

    Ok(())
}
