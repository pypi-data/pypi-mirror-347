# Usage Guide for ebir-automation

This guide demonstrates the main features of the ebir-automation Python package, which automates the eBIRForms application on Windows using Rust and PyO3.

## Basic Usage

```python
from ebir_automation import open_ebir_window_py

# Launch or focus eBIRForms, snap window (default: use_winapi=True, ebir_path=None)
open_ebir_window_py()
```

## Full API Example

```python
from ebir_automation import (
    open_ebir_window_py,
    type_tin_py,
    navigate_to_section_py,
    click_button_py,
    select_tax_type_py,
    set_accept_terms_py,
    complete_form_py,
    SECTION_TAXPAYER_INFO,
    SECTION_TAX_TYPE,
    SECTION_PAYMENT_DETAILS,
    SECTION_SUMMARY,
    BUTTON_NEXT,
    BUTTON_PREVIOUS,
    BUTTON_SUBMIT,
    BUTTON_CANCEL,
)

# Launch or focus the application
open_ebir_window_py()

# Fill in TIN fields
type_tin_py("123", "456", "789", "000")

# Navigate to a section
navigate_to_section_py(SECTION_TAXPAYER_INFO)

# Click a button
click_button_py(BUTTON_NEXT)

# Select a tax type
select_tax_type_py("Income Tax")

# Check the accept terms checkbox
set_accept_terms_py(True)

# Complete the form workflow (TIN + tax type + navigation + submit)
complete_form_py("123", "456", "789", "000", "Income Tax")
```

## Constants

- `SECTION_TAXPAYER_INFO`, `SECTION_TAX_TYPE`, `SECTION_PAYMENT_DETAILS`, `SECTION_SUMMARY`
- `BUTTON_NEXT`, `BUTTON_PREVIOUS`, `BUTTON_SUBMIT`, `BUTTON_CANCEL`

## Error Handling

All functions raise `RuntimeError` on failure (e.g., if the eBIRForms window is not found or an element is missing).

## See Also

- [README.md](./README.md) for project overview and installation
- [tests/test_ebir_automation.py](./tests/test_ebir_automation.py) for more examples
