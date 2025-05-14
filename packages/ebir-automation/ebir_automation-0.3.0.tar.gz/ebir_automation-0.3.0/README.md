# ebir-automation

A Python package for robust automation of the eBIRForms application on Windows, powered by Rust, PyO3, and UIAutomation.

## Features

- Launches or focuses the eBIRForms application (including mshta.exe child windows)
- Waits for the application to be fully loaded before proceeding
- Snaps the window to the left half of the screen (Windows 11 supported)
- Reliable window and element polling (no fixed sleeps)
- Python bindings via PyO3
- Automate TIN entry, section navigation, button clicks, tax type selection, and more

## Installation

Install via pip:

```sh
pip install ebir-automation
```

## Usage

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

# Launch or focus eBIRForms, snap window (default: use_winapi=True, ebir_path=None)
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

## Project Links

- Source code: https://github.com/noizrom/ebir-automation
- Issue tracker: https://github.com/noizrom/ebir-automation/issues

## License

MIT
