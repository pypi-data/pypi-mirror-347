# ebir-automation

A Python package for robust automation of the eBIRForms application on Windows, powered by Rust, PyO3, and UIAutomation.

## Features

- Launches or focuses the eBIRForms application (including mshta.exe child windows)
- Waits for the application to be fully loaded before proceeding
- Snaps the window to the left half of the screen (Windows 11 supported)
- Reliable window and element polling (no fixed sleeps)
- Python bindings via PyO3
- Automate TIN entry, form selection, and more

## Installation

Install via pip:

```sh
pip install ebir-automation
```

## Usage

### Basic Example

```python
from ebir_automation import auto_open_ebir_window, EBirformsAutomation

# Launch or focus eBIRForms, snap window (default: use_winapi=True, ebir_path=None)
hwnd = auto_open_ebir_window(True, None)
if hwnd is None:
    raise RuntimeError("Failed to open eBIRForms window")

handle = EBirformsAutomation(hwnd)
handle.type_tin("123", "456", "789", "000")
successful = handle.select_form("1701v2018", fill_up=True)
print("Form selection successful:", successful)
```

### Running the Quick Test Script

A quick test/demo script is provided:

```sh
python -m ebir_automation.quicktest
```

This will launch eBIRForms, enter a sample TIN, and select a form, printing the result.

## API Reference

- `auto_open_ebir_window(use_winapi: bool = True, ebir_path: Optional[str] = None) -> int | None`
  - Launch or focus the eBIRForms application and return its window handle, or None on failure.
- `class EBirformsAutomation(hwnd: int)`
  - `.type_tin(tin1: str, tin2: str, tin3: str, tin4: str) -> None`
  - `.select_form(form: str, fill_up: bool) -> bool`

## Error Handling

All functions raise `RuntimeError` on failure (e.g., if the eBIRForms window is not found or an element is missing).

## Project Links

- Source code: https://github.com/noizrom/ebir-automation
- Issue tracker: https://github.com/noizrom/ebir-automation/issues

## License

MIT
