from . import EBirformsAutomation
from . import auto_open_ebir_window


def main():
    hwnd = auto_open_ebir_window(True, None)
    if hwnd is None:
        print("Failed to open eBIRForms window")
        return

    handle = EBirformsAutomation(hwnd)
    handle.type_tin("004", "185", "403", "000")
    successful = handle.select_form("1701v2018", fill_up=True)
    print("Form selection successful:", successful)


if __name__ == "__main__":
    main()
