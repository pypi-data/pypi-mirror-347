// Higher-Level flows (e.g. Login, Submit, Set text etc)
use crate::constants::{TIN1_ID, TIN2_ID, TIN3_ID, TIN4_ID};
use crate::{automation_utils, click, find_by_id, send_keys, set_value};
use uiautomation::UIAutomation;
use uiautomation::UIElement;

/// Error type for workflow operations
#[derive(Debug)]
pub enum WorkflowError {
    /// UI Automation error
    UIAutomation(uiautomation::errors::Error),
    /// Window not found
    WindowNotFound,
    /// Element not found
    ElementNotFound(String),
    /// Timeout waiting for an element
    Timeout(String),
    /// Other error
    Other(String),
}

impl From<uiautomation::errors::Error> for WorkflowError {
    fn from(err: uiautomation::errors::Error) -> Self {
        WorkflowError::UIAutomation(err)
    }
}

impl From<String> for WorkflowError {
    fn from(err: String) -> Self {
        WorkflowError::Other(err)
    }
}

fn find_with_retry<'a>(
    uia: &'a UIAutomation,
    root: &'a UIElement,
) -> impl Fn(&str) -> Result<UIElement, WorkflowError> + 'a {
    move |id: &str| {
        automation_utils::retry(
            || find_by_id!(uia, root, id).map_err(|e| e),
            10,  // Max attempts
            500, // Retry delay in ms
        )
        .map_err(|e| {
            WorkflowError::ElementNotFound(format!("Failed to find element '{}': {:?}", id, e))
        })
    }
}

fn find_classname_with_retry(
    uia: &UIAutomation,
    root: &UIElement,
    class_name: &str,
) -> Result<UIElement, WorkflowError> {
    use std::time::{Duration, Instant};
    use uiautomation::types::TreeScope;
    let condition = uia
        .create_property_condition(
            uiautomation::types::UIProperty::ClassName,
            uiautomation::variants::Variant::from(class_name),
            None,
        )
        .map_err(WorkflowError::UIAutomation)?;
    let start = Instant::now();
    let timeout = Duration::from_secs(120);
    let poll_interval = Duration::from_millis(500);
    while start.elapsed() < timeout {
        if let Ok(element) = root.find_first(TreeScope::Descendants, &condition) {
            return Ok(element);
        }
        std::thread::sleep(poll_interval);
    }
    Err(WorkflowError::Timeout(format!(
        "Timeout waiting for class '{}'.",
        class_name
    )))
}

/// Type a TIN (Tax Identification Number) in the form
///
/// # Arguments
/// * `tin1` - First part of the TIN
/// * `tin2` - Second part of the TIN
/// * `tin3` - Third part of the TIN
/// * `tin4` - Fourth part of the TIN
/// * `hwnd` - Window handle of the eBIRForms application
pub fn type_tin(
    tin1: &str,
    tin2: &str,
    tin3: &str,
    tin4: &str,
    uia: &UIAutomation,
    root: &UIElement,
) -> Result<(), WorkflowError> {
    println!("Found window: {:?}", root.get_name());

    let find_with_retry = find_with_retry(uia, root);

    // Find all TIN fields with retry logic
    let tin1_element = find_with_retry(TIN1_ID)?;
    let tin2_element = find_with_retry(TIN2_ID)?;
    let tin3_element = find_with_retry(TIN3_ID)?;
    let tin4_element = find_with_retry(TIN4_ID)?;

    // Set values using the set_value! macro
    set_value!(tin1_element, tin1)?;
    set_value!(tin2_element, tin2)?;
    set_value!(tin3_element, tin3)?;
    set_value!(tin4_element, tin4)?;

    send_keys!(tin4_element, "{tab}{tab}", Some(300u64))?;
    Ok(())
}

// Fix Clippy warnings for unused variables in select_form
pub fn select_form(
    _form: &str,
    _fill_up: bool,
    uia: &UIAutomation,
    root: &UIElement,
) -> Result<bool, WorkflowError> {
    println!("Found window: {:?}", root.get_name());

    let find_with_retry = find_with_retry(uia, root);
    let form_type = find_with_retry("btnFallOut")?;
    click!(form_type)?;

    let fillup = find_with_retry("btnFillup")?;
    click!(fillup)?;

    // wait for ClassName	#32770 for 120 seconds if not, throw WorkflowError
    let _ = find_classname_with_retry(uia, root, "#32770")?;
    // within dialog click (title="OK", auto_id="2", control_type="Button")
    let ok = find_with_retry("2")?; // auto_id="2"
    click!(ok)?;
    Ok(true)
}
