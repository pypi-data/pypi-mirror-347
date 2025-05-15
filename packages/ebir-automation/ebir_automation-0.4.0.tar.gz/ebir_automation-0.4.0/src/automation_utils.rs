// Contains core reusable functions for automating the app (find, click , set, wait etc)

use std::thread;
use std::time::Duration;
use uiautomation::{
    UIAutomation, UIElement,
    controls::ControlType,
    core::UICondition,
    patterns::{UIInvokePattern, UISelectionItemPattern, UITogglePattern, UIValuePattern},
    types::{TreeScope, UIProperty},
    variants::Variant,
};

/// Creates a condition to find an element by its automation ID.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `automation_id` - The automation ID to search for.
///
/// # Returns
/// A UICondition that can be used to find elements with the specified automation ID.
pub fn create_automation_id_condition(
    uia: &UIAutomation,
    automation_id: &str,
) -> Result<UICondition, uiautomation::errors::Error> {
    uia.create_property_condition(UIProperty::AutomationId, Variant::from(automation_id), None)
}

/// Creates a condition to find an element by its control type.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `control_type` - The control type to search for.
///
/// # Returns
/// A UICondition that can be used to find elements with the specified control type.
pub fn create_control_type_condition(
    uia: &UIAutomation,
    control_type: ControlType,
) -> Result<UICondition, uiautomation::errors::Error> {
    uia.create_property_condition(
        UIProperty::ControlType,
        Variant::from(control_type as i32),
        None,
    )
}

/// Creates a condition to find an element by its name.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `name` - The name to search for.
///
/// # Returns
/// A UICondition that can be used to find elements with the specified name.
pub fn create_name_condition(
    uia: &UIAutomation,
    name: &str,
) -> Result<UICondition, uiautomation::errors::Error> {
    uia.create_property_condition(UIProperty::Name, Variant::from(name), None)
}

/// Finds a UI element by its automation ID within a parent element.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `parent` - The parent element to search within.
/// * `automation_id` - The automation ID to search for.
/// * `scope` - The scope of the search (e.g., TreeScope::Descendants).
///
/// # Returns
/// The found UI element or an error if not found.
pub fn find_element_by_automation_id(
    uia: &UIAutomation,
    parent: &UIElement,
    automation_id: &str,
    scope: TreeScope,
) -> Result<UIElement, uiautomation::errors::Error> {
    let condition = create_automation_id_condition(uia, automation_id)?;
    parent.find_first(scope, &condition)
}

/// Finds a UI element by its name within a parent element.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `parent` - The parent element to search within.
/// * `name` - The name to search for.
/// * `scope` - The scope of the search (e.g., TreeScope::Descendants).
///
/// # Returns
/// The found UI element or an error if not found.
pub fn find_element_by_name(
    uia: &UIAutomation,
    parent: &UIElement,
    name: &str,
    scope: TreeScope,
) -> Result<UIElement, uiautomation::errors::Error> {
    let condition = create_name_condition(uia, name)?;
    parent.find_first(scope, &condition)
}

/// Finds a UI element by its control type within a parent element.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `parent` - The parent element to search within.
/// * `control_type` - The control type to search for.
/// * `scope` - The scope of the search (e.g., TreeScope::Descendants).
///
/// # Returns
/// The found UI element or an error if not found.
pub fn find_element_by_control_type(
    uia: &UIAutomation,
    parent: &UIElement,
    control_type: ControlType,
    scope: TreeScope,
) -> Result<UIElement, uiautomation::errors::Error> {
    let condition = create_control_type_condition(uia, control_type)?;
    parent.find_first(scope, &condition)
}

/// Sets a text value on a UI element that supports the Value pattern.
///
/// # Arguments
/// * `element` - The element to set the value on.
/// * `value` - The text value to set.
///
/// # Returns
/// Result indicating success or failure.
pub fn set_element_value(
    element: &UIElement,
    value: &str,
) -> Result<(), uiautomation::errors::Error> {
    let pattern = element.get_pattern::<UIValuePattern>()?;
    pattern.set_value(value)
}

/// Sends keys to a UI element.
///
/// # Arguments
/// * `element` - The element to send keys to.
/// * `keys` - The keys to send.
///
/// # Returns
/// Result indicating success or failure.
pub fn send_keys_to_element(
    element: &UIElement,
    keys: &str,
    interval: Option<u64>,
) -> Result<(), uiautomation::errors::Error> {
    let interval = interval.unwrap_or(50);
    element.send_keys(keys, interval)
}

/// Clicks a UI element that supports the Invoke pattern (e.g., buttons).
///
/// # Arguments
/// * `element` - The element to click.
///
/// # Returns
/// Result indicating success or failure.
pub fn click_element(element: &UIElement) -> Result<(), uiautomation::errors::Error> {
    let pattern = element.get_pattern::<UIInvokePattern>()?;
    pattern.invoke()
}

/// Toggles a UI element that supports the Toggle pattern (e.g., checkboxes).
///
/// # Arguments
/// * `element` - The element to toggle.
///
/// # Returns
/// Result indicating success or failure.
pub fn toggle_element(element: &UIElement) -> Result<(), uiautomation::errors::Error> {
    let pattern = element.get_pattern::<UITogglePattern>()?;
    pattern.toggle()
}

/// Selects a UI element that supports the SelectionItem pattern (e.g., combo box items).
///
/// # Arguments
/// * `element` - The element to select.
///
/// # Returns
/// Result indicating success or failure.
pub fn select_element(element: &UIElement) -> Result<(), uiautomation::errors::Error> {
    let pattern = element.get_pattern::<UISelectionItemPattern>()?;
    pattern.select()
}

/// Waits for an element to become available by polling with a specified interval.
///
/// # Arguments
/// * `find_fn` - A closure that attempts to find the element.
/// * `timeout_ms` - Maximum time to wait in milliseconds.
/// * `interval_ms` - Polling interval in milliseconds.
///
/// # Returns
/// The found element or an error if timed out.
pub fn wait_for_element<F, E>(
    mut find_fn: F,
    timeout_ms: u64,
    interval_ms: u64,
) -> Result<UIElement, String>
where
    F: FnMut() -> Result<UIElement, E>,
    E: std::fmt::Debug,
{
    let start_time = std::time::Instant::now();
    let timeout = Duration::from_millis(timeout_ms);

    loop {
        match find_fn() {
            Ok(element) => return Ok(element),
            Err(e) => {
                if start_time.elapsed() > timeout {
                    return Err(format!("Timed out waiting for element: {:?}", e));
                }
                thread::sleep(Duration::from_millis(interval_ms));
            }
        }
    }
}

/// Performs an action with retry logic.
///
/// # Arguments
/// * `action` - A closure that performs the action.
/// * `max_attempts` - Maximum number of attempts.
/// * `retry_delay_ms` - Delay between retries in milliseconds.
///
/// # Returns
/// The result of the action or the last error encountered.
pub fn retry<T, E, F>(mut action: F, max_attempts: u32, retry_delay_ms: u64) -> Result<T, E>
where
    F: FnMut() -> Result<T, E>,
    E: std::fmt::Debug,
{
    let mut attempts = 0;
    let retry_delay = Duration::from_millis(retry_delay_ms);

    loop {
        match action() {
            Ok(result) => return Ok(result),
            Err(e) => {
                attempts += 1;
                if attempts >= max_attempts {
                    return Err(e);
                }
                thread::sleep(retry_delay);
            }
        }
    }
}

/// Macro to create and find a UI element by automation ID with error handling.
///
/// # Example
/// ```
/// let tin1_element = find_by_id!(uia, window, "tin1")?;
/// ```
#[macro_export]
macro_rules! find_by_id {
    ($uia:expr, $parent:expr, $id:expr) => {
        $crate::automation_utils::find_element_by_automation_id(
            &$uia,
            &$parent,
            $id,
            uiautomation::types::TreeScope::Descendants,
        )
    };
}

/// Macro to create and find a UI element by name with error handling.
///
/// # Example
/// ```
/// let save_element = find_by_name!(uia, window, "Save")?;
/// ```
#[macro_export]
macro_rules! find_by_name {
    ($uia:expr, $parent:expr, $name:expr) => {
        $crate::automation_utils::find_element_by_name(
            &$uia,
            &$parent,
            $name,
            uiautomation::types::TreeScope::Descendants,
        )
    };
}

/// Macro to set a value on a UI element that supports the Value pattern with error handling.
///
/// # Example
/// ```
/// set_value!(element, "text to set")?;
/// ```
#[macro_export]
macro_rules! set_value {
    ($element:expr, $value:expr) => {
        $crate::automation_utils::set_element_value(&$element, $value)
    };
}

/// Macro to send keys to a UI element with error handling.
///
/// # Example
/// ```
/// send_keys!(element, "{tab}{tab}")?;
/// ```
#[macro_export]
macro_rules! send_keys {
    ($element:expr, $keys:expr, $interval:expr) => {
        $crate::automation_utils::send_keys_to_element(&$element, $keys, $interval)
    };
}

/// Macro to click a UI element with error handling.
///
/// # Example
/// ```
/// click!(button_element)?;
/// ```
#[macro_export]
macro_rules! click {
    ($element:expr) => {
        $crate::automation_utils::click_element(&$element)
    };
}

/// Macro to toggle a UI element with error handling.
///
/// # Example
/// ```
/// toggle!(checkbox_element)?;
/// ```
#[macro_export]
macro_rules! toggle {
    ($element:expr) => {
        $crate::automation_utils::toggle_element(&$element)
    };
}

/// Macro to select a UI element with error handling.
///
/// # Example
/// ```
/// select!(list_item_element)?;
/// ```
#[macro_export]
macro_rules! select {
    ($element:expr) => {
        $crate::automation_utils::select_element(&$element)
    };
}

/// Macro to create and find a combobox UI element by automation ID with error handling.
///
/// # Example
/// ```
/// let combo_element = find_combobox!(uia, window, "comboId")?;
/// ```
#[macro_export]
macro_rules! find_combobox {
    ($uia:expr, $parent:expr, $id:expr) => {
        $crate::automation_utils::find_combobox_by_id(
            &$uia,
            &$parent,
            $id,
            uiautomation::types::TreeScope::Descendants,
        )
    };
}

/// Macro to create and find a checkbox UI element by automation ID with error handling.
///
/// # Example
/// ```
/// let checkbox_element = find_checkbox!(uia, window, "checkboxId")?;
/// ```
#[macro_export]
macro_rules! find_checkbox {
    ($uia:expr, $parent:expr, $id:expr) => {
        $crate::automation_utils::find_checkbox_by_id(
            &$uia,
            &$parent,
            $id,
            uiautomation::types::TreeScope::Descendants,
        )
    };
}

/// Macro to create and find a button UI element by automation ID with error handling.
///
/// # Example
/// ```
/// let button_element = find_button!(uia, window, "buttonId")?;
/// ```
#[macro_export]
macro_rules! find_button {
    ($uia:expr, $parent:expr, $id:expr) => {
        $crate::automation_utils::find_button_by_id(
            &$uia,
            &$parent,
            $id,
            uiautomation::types::TreeScope::Descendants,
        )
    };
}

/// Macro to select an item from a combobox by name with error handling.
///
/// # Example
/// ```
/// select_combobox_item!(uia, combobox_element, "item name")?;
/// ```
#[macro_export]
macro_rules! select_combobox_item {
    ($uia:expr, $combobox:expr, $name:expr) => {
        $crate::automation_utils::select_combobox_item_by_name(&$uia, &$combobox, $name)
    };
}

/// Macro to set a checkbox state (checked or unchecked) with error handling.
///
/// # Example
/// ```
/// set_checkbox!(checkbox_element, true)?; // Check
/// set_checkbox!(checkbox_element, false)?; // Uncheck
/// ```
#[macro_export]
macro_rules! set_checkbox {
    ($checkbox:expr, $check:expr) => {
        $crate::automation_utils::set_checkbox_state(&$checkbox, $check)
    };
}

/// Finds a UI element by its automation ID and control type within a parent element.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `parent` - The parent element to search within.
/// * `automation_id` - The automation ID to search for.
/// * `control_type` - The control type to search for.
/// * `scope` - The scope of the search (e.g., TreeScope::Descendants).
///
/// # Returns
/// The found UI element or an error if not found.
pub fn find_element_by_id_and_type(
    uia: &UIAutomation,
    parent: &UIElement,
    automation_id: &str,
    control_type: ControlType,
    scope: TreeScope,
) -> Result<UIElement, uiautomation::errors::Error> {
    // Create condition for automation ID
    let id_condition = create_automation_id_condition(uia, automation_id)?;

    // Create condition for control type
    let type_condition = create_control_type_condition(uia, control_type)?;

    // Combine conditions with AND
    let combined_condition = uia.create_and_condition(id_condition, type_condition)?;

    // Find element
    parent.find_first(scope, &combined_condition)
}

/// Finds a combobox element by its automation ID within a parent element.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `parent` - The parent element to search within.
/// * `automation_id` - The automation ID to search for.
/// * `scope` - The scope of the search (e.g., TreeScope::Descendants).
///
/// # Returns
/// The found combobox element or an error if not found.
pub fn find_combobox_by_id(
    uia: &UIAutomation,
    parent: &UIElement,
    automation_id: &str,
    scope: TreeScope,
) -> Result<UIElement, uiautomation::errors::Error> {
    find_element_by_id_and_type(uia, parent, automation_id, ControlType::ComboBox, scope)
}

/// Finds a checkbox element by its automation ID within a parent element.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `parent` - The parent element to search within.
/// * `automation_id` - The automation ID to search for.
/// * `scope` - The scope of the search (e.g., TreeScope::Descendants).
///
/// # Returns
/// The found checkbox element or an error if not found.
pub fn find_checkbox_by_id(
    uia: &UIAutomation,
    parent: &UIElement,
    automation_id: &str,
    scope: TreeScope,
) -> Result<UIElement, uiautomation::errors::Error> {
    find_element_by_id_and_type(uia, parent, automation_id, ControlType::CheckBox, scope)
}

/// Finds a button element by its automation ID within a parent element.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `parent` - The parent element to search within.
/// * `automation_id` - The automation ID to search for.
/// * `scope` - The scope of the search (e.g., TreeScope::Descendants).
///
/// # Returns
/// The found button element or an error if not found.
pub fn find_button_by_id(
    uia: &UIAutomation,
    parent: &UIElement,
    automation_id: &str,
    scope: TreeScope,
) -> Result<UIElement, uiautomation::errors::Error> {
    find_element_by_id_and_type(uia, parent, automation_id, ControlType::Button, scope)
}

/// Selects an item from a combobox by index.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `combobox` - The combobox element.
/// * `index` - The index of the item to select (0-based).
///
/// # Returns
/// Result indicating success or failure.
pub fn select_combobox_item_by_index(
    uia: &UIAutomation,
    combobox: &UIElement,
    index: usize,
) -> Result<(), uiautomation::errors::Error> {
    use uiautomation::patterns::UIExpandCollapsePattern;

    // Expand the combobox to show items
    let expand_pattern = combobox.get_pattern::<UIExpandCollapsePattern>()?;
    expand_pattern.expand()?;

    // Wait for the items to appear
    thread::sleep(Duration::from_millis(300));

    // Get all items
    let items_condition = create_control_type_condition(uia, ControlType::ListItem)?;
    let items = combobox.find_all(TreeScope::Descendants, &items_condition)?; // Check if index is valid
    if index >= items.len() {
        return Err(uiautomation::errors::Error::new(-1, "Index out of bounds"));
    }

    // Select the item by index
    let item = items
        .get(index)
        .ok_or_else(|| uiautomation::errors::Error::new(-1, "Failed to get item by index"))?;
    select_element(item)?;

    Ok(())
}

/// Selects an item from a combobox by name.
///
/// # Arguments
/// * `uia` - The UI Automation instance.
/// * `combobox` - The combobox element.
/// * `name` - The name of the item to select.
///
/// # Returns
/// Result indicating success or failure.
pub fn select_combobox_item_by_name(
    uia: &UIAutomation,
    combobox: &UIElement,
    name: &str,
) -> Result<(), uiautomation::errors::Error> {
    use uiautomation::patterns::UIExpandCollapsePattern;

    // Expand the combobox to show items
    let expand_pattern = combobox.get_pattern::<UIExpandCollapsePattern>()?;
    expand_pattern.expand()?;

    // Wait for the items to appear
    thread::sleep(Duration::from_millis(300));

    // Find the item by name
    let name_condition = create_name_condition(uia, name)?;
    let item = combobox.find_first(TreeScope::Descendants, &name_condition)?;

    // Select the item
    select_element(&item)?;

    Ok(())
}

/// Checks or unchecks a checkbox.
///
/// # Arguments
/// * `checkbox` - The checkbox element.
/// * `check` - Whether to check (true) or uncheck (false) the checkbox.
///
/// # Returns
/// Result indicating success or failure.
pub fn set_checkbox_state(
    checkbox: &UIElement,
    check: bool,
) -> Result<(), uiautomation::errors::Error> {
    use uiautomation::patterns::UITogglePattern;

    let toggle_pattern = checkbox.get_pattern::<UITogglePattern>()?;
    let current_state = toggle_pattern.get_toggle_state()?;
    use uiautomation::types::ToggleState;
    // Convert ToggleState to a boolean
    let is_checked = current_state == ToggleState::On;
    // If current state doesn't match desired state, toggle it
    if is_checked != check {
        toggle_pattern.toggle()?;
    }
    Ok(())
}
