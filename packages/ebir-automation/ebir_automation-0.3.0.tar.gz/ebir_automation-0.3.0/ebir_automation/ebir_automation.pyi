# This file provides type hints for the ebir_automation Python extension module built with PyO3.
# Place this file alongside the generated ebir_automation.pyd/.dll in your package directory.

from typing import Optional

def open_ebir_window_py(
    use_winapi: Optional[bool] = ..., ebir_path: Optional[str] = ...
) -> None: ...
def type_tin_py(tin1: str, tin2: str, tin3: str, tin4: str) -> None: ...
def navigate_to_section_py(section_name: str) -> None: ...
def click_button_py(button_name: str) -> None: ...
def select_tax_type_py(tax_type: str) -> None: ...
def set_accept_terms_py(check: bool) -> None: ...
def complete_form_py(
    tin1: str, tin2: str, tin3: str, tin4: str, tax_type: str
) -> None: ...

# Module-level constants for sections
SECTION_TAXPAYER_INFO: str
SECTION_TAX_TYPE: str
SECTION_PAYMENT_DETAILS: str
SECTION_SUMMARY: str

# Module-level constants for buttons
BUTTON_NEXT: str
BUTTON_PREVIOUS: str
BUTTON_SUBMIT: str
BUTTON_CANCEL: str
