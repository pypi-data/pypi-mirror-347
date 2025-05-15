from ebir_automation import auto_open_ebir_window, EBirformsAutomation


def test_main_page_workflow():
    hwnd = auto_open_ebir_window(True, None)
    assert hwnd is not None

    handle = EBirformsAutomation(hwnd)
    handle.type_tin("004", "185", "403", "000")
    successful = handle.select_form("1701v2018", fill_up=True)
    assert successful is True
