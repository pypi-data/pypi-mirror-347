// Higher-Level flows (e.g. Login, Submit, Set text etc)
use crate::{automation_utils, click, find_by_id, find_by_name, set_value};
use crate::constants::{TIN1_ID, TIN2_ID, TIN3_ID, TIN4_ID, BUTTON_NEXT, SECTION_TAXPAYER_INFO};
use std::time::Duration;
use uiautomation::{types::Handle, UIAutomation};
use windows::Win32::Foundation::HWND;

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

/// Type a TIN (Tax Identification Number) in the form
///
/// # Arguments
/// * `tin1` - First part of the TIN
/// * `tin2` - Second part of the TIN
/// * `tin3` - Third part of the TIN
/// * `tin4` - Fourth part of the TIN
/// * `hwnd` - Window handle of the eBIRForms application
pub fn type_tin(tin1: &str, tin2: &str, tin3: &str, tin4: &str, hwnd: HWND) {
    let uia = UIAutomation::new().expect("Failed to initialize UI Automation");
    let handle = Handle::from(hwnd.0);
    
    match uia.element_from_handle(handle) {
        Ok(window) => {
            println!("Found window: {:?}", window.get_name());

            // Find elements and set values using utility functions and macros
            let result = (|| -> Result<(), WorkflowError> {
                // Navigate to the taxpayer information section if not already there
                match find_by_name!(uia, window, SECTION_TAXPAYER_INFO) {
                    Ok(section) => {
                        let _ = click!(section);
                        // Small delay to let UI update
                        std::thread::sleep(Duration::from_millis(500));
                    },
                    Err(_) => {
                        // Section may already be active or have a different ID
                        println!("Could not find Taxpayer Information section, continuing with TIN entry");
                    }
                }
                
                // Use retry logic to handle potential timing issues
                let find_with_retry = |id: &str| {
                    automation_utils::retry(
                        || find_by_id!(uia, window, id).map_err(|e| e),
                        3,  // Max attempts
                        500, // Retry delay in ms
                    )
                    .map_err(|e| WorkflowError::ElementNotFound(format!("Failed to find element '{}': {:?}", id, e)))
                };

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
                
                // Try to click Next button if available
                if let Ok(next_button) = find_by_name!(uia, window, BUTTON_NEXT) {
                    let _ = click!(next_button);
                }
                
                Ok(())
            })();

            if let Err(e) = result {
                eprintln!("Error typing TIN: {:?}", e);
            } else {
                println!("Successfully entered TIN");
            }
        }
        Err(_) => eprintln!("Failed to find window"),
    }
}

/// Navigate to a form section by name
///
/// # Arguments
/// * `section_name` - The name of the section to navigate to
/// * `hwnd` - Window handle of the eBIRForms application
pub fn navigate_to_section(section_name: &str, hwnd: HWND) -> Result<(), WorkflowError> {
    let uia = UIAutomation::new().expect("Failed to initialize UI Automation");
    let handle = Handle::from(hwnd.0);
    
    let window = uia.element_from_handle(handle)
        .map_err(|_| WorkflowError::WindowNotFound)?;
    
    println!("Navigating to section: {}", section_name);
      // Wait for the navigation menu to be available
    let section = automation_utils::wait_for_element(
        || find_by_name!(uia, window, section_name),
        5000, // 5 second timeout
        100,  // 100ms interval
    ).map_err(WorkflowError::Timeout)?;
    
    // Click on the section
    click!(section)?;
    
    // Small delay to allow UI to update
    std::thread::sleep(Duration::from_millis(500));
    
    Ok(())
}

/// Click a button by name
///
/// # Arguments
/// * `button_name` - The name of the button to click
/// * `hwnd` - Window handle of the eBIRForms application
pub fn click_button(button_name: &str, hwnd: HWND) -> Result<(), WorkflowError> {
    let uia = UIAutomation::new().expect("Failed to initialize UI Automation");
    let handle = Handle::from(hwnd.0);
    
    let window = uia.element_from_handle(handle)
        .map_err(|_| WorkflowError::WindowNotFound)?;
    
    println!("Clicking button: {}", button_name);
    
    // Find the button with retry logic
    let button = automation_utils::retry(
        || find_by_name!(uia, window, button_name).map_err(|e| e),
        3,  // Max attempts
        500, // Retry delay in ms
    )
    .map_err(|e| WorkflowError::ElementNotFound(format!("Button '{}' not found: {:?}", button_name, e)))?;
    
    // Click the button
    click!(button)?;
    
    Ok(())
}

/// Complete the basic form workflow from TIN entry to submission
///
/// # Arguments
/// * `tin1` - First part of the TIN
/// * `tin2` - Second part of the TIN
/// * `tin3` - Third part of the TIN
/// * `tin4` - Fourth part of the TIN
/// * `hwnd` - Window handle of the eBIRForms application
pub fn complete_form(tin1: &str, tin2: &str, tin3: &str, tin4: &str, tax_type: &str, hwnd: HWND) -> Result<(), WorkflowError> {
    use crate::constants::{SECTION_TAXPAYER_INFO, SECTION_TAX_TYPE, SECTION_PAYMENT_DETAILS, SECTION_SUMMARY, BUTTON_NEXT, BUTTON_SUBMIT};
    
    // Step 1: Navigate to taxpayer info and enter TIN
    navigate_to_section(SECTION_TAXPAYER_INFO, hwnd)?;
    type_tin(tin1, tin2, tin3, tin4, hwnd);
    
    // Step 2: Navigate to tax type and select options
    navigate_to_section(SECTION_TAX_TYPE, hwnd)?;
    select_tax_type(tax_type, hwnd)?;
    click_button(BUTTON_NEXT, hwnd)?;
    
    // Step 3: Enter payment details (placeholder)
    navigate_to_section(SECTION_PAYMENT_DETAILS, hwnd)?;
    click_button(BUTTON_NEXT, hwnd)?;
    
    // Step 4: Review summary, accept terms, and submit
    navigate_to_section(SECTION_SUMMARY, hwnd)?;
    set_accept_terms(true, hwnd)?;
    click_button(BUTTON_SUBMIT, hwnd)?;
    
    Ok(())
}

/// Select a tax type from the dropdown
///
/// # Arguments
/// * `tax_type` - The tax type to select
/// * `hwnd` - Window handle of the eBIRForms application
pub fn select_tax_type(tax_type: &str, hwnd: HWND) -> Result<(), WorkflowError> {
    use crate::{constants::DROPDOWN_TAX_TYPE, constants::SECTION_TAX_TYPE, find_combobox, select_combobox_item};
    
    let uia = UIAutomation::new().expect("Failed to initialize UI Automation");
    let handle = Handle::from(hwnd.0);
    
    let window = uia.element_from_handle(handle)
        .map_err(|_| WorkflowError::WindowNotFound)?;
    
    // Navigate to the tax type section
    navigate_to_section(SECTION_TAX_TYPE, hwnd)?;
    
    println!("Selecting tax type: {}", tax_type);
    
    // Find the tax type dropdown
    let dropdown = find_combobox!(uia, window, DROPDOWN_TAX_TYPE)
        .map_err(|e| WorkflowError::ElementNotFound(format!("Tax type dropdown not found: {:?}", e)))?;
    
    // Select the tax type
    select_combobox_item!(uia, dropdown, tax_type)
        .map_err(|e| WorkflowError::Other(format!("Failed to select tax type '{}': {:?}", tax_type, e)))?;
    
    Ok(())
}

/// Check or uncheck the 'Accept Terms' checkbox
///
/// # Arguments
/// * `check` - Whether to check (true) or uncheck (false) the checkbox
/// * `hwnd` - Window handle of the eBIRForms application
pub fn set_accept_terms(check: bool, hwnd: HWND) -> Result<(), WorkflowError> {
    use crate::{constants::CHECKBOX_ACCEPT_TERMS, constants::SECTION_SUMMARY, find_checkbox, set_checkbox};
    
    let uia = UIAutomation::new().expect("Failed to initialize UI Automation");
    let handle = Handle::from(hwnd.0);
    
    let window = uia.element_from_handle(handle)
        .map_err(|_| WorkflowError::WindowNotFound)?;
    
    // Navigate to the summary section where accept terms is located
    navigate_to_section(SECTION_SUMMARY, hwnd)?;
    
    println!("{} accept terms checkbox", if check { "Checking" } else { "Unchecking" });
    
    // Find the accept terms checkbox
    let checkbox = find_checkbox!(uia, window, CHECKBOX_ACCEPT_TERMS)
        .map_err(|e| WorkflowError::ElementNotFound(format!("Accept terms checkbox not found: {:?}", e)))?;
    
    // Set the checkbox state
    set_checkbox!(checkbox, check)
        .map_err(|e| WorkflowError::Other(format!("Failed to set accept terms checkbox: {:?}", e)))?;
    
    Ok(())
}
