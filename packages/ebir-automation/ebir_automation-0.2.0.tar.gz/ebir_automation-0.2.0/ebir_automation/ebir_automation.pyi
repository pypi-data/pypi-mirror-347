# This file provides type hints for the ebir_automation Python extension module built with PyO3.
# Place this file alongside the generated ebir_automation.pyd/.dll in your package directory.

from typing import Optional

def open_ebir_window_py(
    use_winapi: Optional[bool] = ..., ebir_path: Optional[str] = ...
) -> None: ...
