# ebir-automation

A Python package for robust automation of the eBIRForms application on Windows, powered by Rust, PyO3, and UIAutomation.

## Features

- Launches or focuses the eBIRForms application (including mshta.exe child windows)
- Waits for the application to be fully loaded before proceeding
- Snaps the window to the left half of the screen (Windows 11 supported)
- Reliable window and element polling (no fixed sleeps)
- Python bindings via PyO3

## Installation

Install via pip:

```sh
pip install ebir-automation
```

## Usage

```python
from ebir_automation import open_ebir_window_py

# Launch or focus eBIRForms, snap window (default: use_winapi=True, ebir_path=None)
open_ebir_window_py()

# With custom options:
open_ebir_window_py(use_winapi=False, ebir_path=r"C:\\eBIRForms\\BIRForms.exe")
```

## Project Links

- Source code: https://github.com/noizrom/ebir-automation
- Issue tracker: https://github.com/noizrom/ebir-automation/issues

## License

MIT
