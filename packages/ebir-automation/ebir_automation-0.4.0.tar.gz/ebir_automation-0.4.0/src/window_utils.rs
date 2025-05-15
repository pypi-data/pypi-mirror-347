//! Utilities for automating and managing eBIRForms and related windows.
use std::env;
use std::process::Command;
use std::{
    thread,
    time::{Duration, Instant},
};
use uiautomation::{UIAutomation, types::Handle};
use windows::Win32::UI::Input::KeyboardAndMouse::{
    INPUT, INPUT_0, INPUT_KEYBOARD, KEYBD_EVENT_FLAGS, KEYBDINPUT, SendInput, VIRTUAL_KEY,
};

use crate::constants::{
    DEFAULT_APP_PATH, EBIRFORMS_CLASS_NAME, EBIRFORMS_PROCESS_NAME, SNAP_KEY_DELAY, VK_1,
    VK_ESCAPE, VK_LWIN, VK_Z,
};
use sysinfo::{ProcessRefreshKind, ProcessesToUpdate, System};
use windows::{
    Win32::Foundation::{BOOL, HWND, LPARAM},
    Win32::UI::WindowsAndMessaging::{
        EnumWindows, FindWindowW, GetWindowThreadProcessId, IsWindowVisible,
    },
    core::PCWSTR,
};

// eBIRForms application specific constants

/// Find the HWND of the first visible window belonging to a process with the given name (case-insensitive).
/// Returns `Some(HWND)` if found, or `None` if not found.
fn find_hwnd_by_process_name(process_name: &str) -> Option<HWND> {
    find_pid_by_name(process_name).and_then(find_hwnd_by_pid)
}

/// Find the PID of the first process with the given name (case-insensitive).
/// Returns `Some(pid)` if found, or `None` if not found.
fn find_pid_by_name(process_name: &str) -> Option<u32> {
    let mut system = System::new_all();
    system.refresh_processes_specifics(
        ProcessesToUpdate::All,
        true,
        ProcessRefreshKind::everything(),
    );
    for (pid, process) in system.processes() {
        if process.name().eq_ignore_ascii_case(process_name) {
            return Some(pid.as_u32());
        }
    }
    None
}

/// Find a window handle (HWND) belonging to a process with the specified PID.
/// Enumerates all top-level windows and returns the first visible window for the PID.
fn find_hwnd_by_pid(pid: u32) -> Option<HWND> {
    // Create a context structure to safely pass data through the callback
    struct Context {
        target_pid: u32,
        result_hwnd: HWND,
    }

    // Callback function for EnumWindows
    unsafe extern "system" fn enum_windows_proc(hwnd: HWND, lparam: LPARAM) -> BOOL {
        // Safety: We trust that EnumWindows gives us a valid LPARAM that points to our Context
        unsafe {
            let context = &mut *(lparam.0 as *mut Context);
            let mut pid = 0;

            // Safety: GetWindowThreadProcessId is an FFI call that requires unsafe
            GetWindowThreadProcessId(hwnd, Some(&mut pid));

            // Safety: IsWindowVisible is an FFI call that requires unsafe
            if pid == context.target_pid && IsWindowVisible(hwnd).as_bool() {
                context.result_hwnd = hwnd;
                return false.into(); // Stop enumeration - window found
            }

            true.into() // Continue enumeration
        }
    }

    // Initialize context with target PID and null HWND
    let mut context = Context {
        target_pid: pid,
        result_hwnd: HWND(0),
    };

    // Safely pass context to callback through EnumWindows
    // Make sure to handle the Result of EnumWindows
    unsafe {
        // Call EnumWindows. The result will be in context.hwnd if a window is found.
        // The return value of EnumWindows itself indicates if the enumeration was completed or stopped.
        // We should handle the Result to address the warning.
        if EnumWindows(
            Some(enum_windows_proc),
            LPARAM(&mut context as *mut _ as isize),
        )
        .is_err()
        {
            // Log an error or handle it appropriately if EnumWindows fails
            eprintln!("EnumWindows call failed during PID search.");
            // Depending on desired behavior, you might return None here or let it proceed
            // to the check of context.result_hwnd. For now, just logging.
        }
    }

    if context.result_hwnd.0 != 0 {
        Some(context.result_hwnd)
    } else {
        None
    }
}

/// Focuses the window with the given HWND. Returns true if successful.
fn focus_window_by_hwnd(hwnd: HWND) -> bool {
    let uia = UIAutomation::new().expect("Failed to initialize UI Automation");
    let handle = Handle::from(hwnd.0);
    match uia.element_from_handle(handle) {
        Ok(window) => {
            println!("Found window: {:?}", window.get_name());
            match window.set_focus() {
                Ok(_) => {
                    unsafe {
                        use windows::Win32::UI::Input::KeyboardAndMouse::SetFocus;
                        use windows::Win32::UI::WindowsAndMessaging::{
                            SW_RESTORE, SetForegroundWindow, ShowWindow,
                        };
                        let _ = ShowWindow(hwnd, SW_RESTORE);
                        let _ = SetForegroundWindow(hwnd);
                        SetFocus(hwnd);
                    }
                    println!("Successfully focused window (UIA + Win32).\n");
                    true
                }
                Err(e) => {
                    eprintln!("Failed to focus window: {:?}", e);
                    false
                }
            }
        }
        Err(_) => false,
    }
}

/// Launches or focuses the eBIRForms application and arranges the mshta.exe window.
///
/// # Arguments
/// * `use_winapi` - If true, use Windows API for window placement; otherwise, use key simulation.
/// * `app_path` - Path to the eBIRForms executable. Defaults to `DEFAULT_APP_PATH` if None.
pub fn open_ebir_window(use_winapi: Option<bool>, app_path: Option<&str>) -> Option<HWND> {
    println!("[START] Launching eBIR application...");
    let start_time = Instant::now();
    let app_path = app_path.unwrap_or(DEFAULT_APP_PATH);

    let bir_hwnd = find_hwnd_by_process_name("BIRForms.exe");
    let bir_pid = bir_hwnd.map(|hwnd| {
        let mut pid = 0;
        unsafe {
            windows::Win32::UI::WindowsAndMessaging::GetWindowThreadProcessId(hwnd, Some(&mut pid));
        }
        pid
    });
    if bir_pid.is_none() {
        // Set working directory to the root of the executable
        let exe_dir = std::path::Path::new(app_path)
            .parent()
            .unwrap_or_else(|| std::path::Path::new("."));
        match Command::new(app_path).current_dir(exe_dir).spawn() {
            Ok(_child) => {
                println!(
                    "[INFO] Process launched in {} ms",
                    start_time.elapsed().as_millis()
                );
                thread::sleep(Duration::from_secs(1)); // Brief pause to let the process start
            }
            Err(e) => {
                eprintln!("[ERROR] Failed to open eBIR: {}", e);
                return None;
            }
        }
    } else {
        println!(
            "[INFO] BIRForms.exe is already running (PID: {:?})",
            bir_pid
        );
    }

    // Use mshta.exe HWND for window operations
    let mshta_hwnd = match find_hwnd_by_process_name("mshta.exe") {
        Some(hwnd) => hwnd,
        None => {
            eprintln!("Could not find mshta.exe window");
            return None;
        }
    };

    if focus_window_by_hwnd(mshta_hwnd) {
        println!("[INFO] Window found and focused, attempting snap...");
        let use_winapi = use_winapi.unwrap_or(true);
        if use_winapi {
            // Place window on left half using Windows API
            use windows::Win32::Foundation::RECT;
            use windows::Win32::UI::WindowsAndMessaging::{
                GetDesktopWindow, GetWindowRect, SWP_SHOWWINDOW, SetWindowPos,
            };
            let mut rect = RECT::default();
            unsafe {
                let desktop = GetDesktopWindow();
                let _ = GetWindowRect(desktop, &mut rect);
                let width = (rect.right - rect.left) / 2;
                let height = rect.bottom - rect.top;
                let _ = SetWindowPos(mshta_hwnd, None, 0, 0, width, height, SWP_SHOWWINDOW);
            }
            println!("[INFO] Window placed using Windows API.");
        } else if is_windows_11() {
            println!("[INFO] Windows 11 detected, sending snap shortcuts...");
            if let Err(e) = send_snap_shortcuts() {
                eprintln!("[ERROR] Failed to send snap shortcuts: {}", e);
            }
        } else {
            println!("[WARN] Windows 11 required for snap feature");
        }
    } else {
        eprintln!("[ERROR] Could not find or focus window");
    }

    println!(
        "[END] Total operation took {} ms",
        start_time.elapsed().as_millis()
    );
    Some(mshta_hwnd)
}

fn send_key(vk: u16, flags: KEYBD_EVENT_FLAGS) -> std::result::Result<(), windows::core::Error> {
    let input = INPUT {
        r#type: INPUT_KEYBOARD,
        Anonymous: INPUT_0 {
            ki: KEYBDINPUT {
                wVk: VIRTUAL_KEY(vk),
                wScan: 0,
                dwFlags: flags,
                time: 0,
                dwExtraInfo: 0,
            },
        },
    };

    unsafe {
        SendInput(&[input], std::mem::size_of::<INPUT>() as i32);
    }
    Ok(())
}

fn send_snap_shortcuts() -> std::result::Result<(), Box<dyn std::error::Error>> {
    println!("[DEBUG] Sending Win+Z");
    // Press Win
    send_key(VK_LWIN, KEYBD_EVENT_FLAGS(0))?;
    // Press Z
    send_key(VK_Z, KEYBD_EVENT_FLAGS(0))?;
    // Release Z
    send_key(VK_Z, KEYBD_EVENT_FLAGS(2))?;
    // Release Win
    send_key(VK_LWIN, KEYBD_EVENT_FLAGS(2))?;

    thread::sleep(SNAP_KEY_DELAY);
    println!("[DEBUG] Sending 1");
    send_key(VK_1, KEYBD_EVENT_FLAGS(0))?;
    send_key(VK_1, KEYBD_EVENT_FLAGS(2))?;

    thread::sleep(SNAP_KEY_DELAY);
    println!("[DEBUG] Sending final 1");
    send_key(VK_1, KEYBD_EVENT_FLAGS(0))?;
    send_key(VK_1, KEYBD_EVENT_FLAGS(2))?;

    // send escape
    thread::sleep(SNAP_KEY_DELAY);
    println!("[DEBUG] Sending escape");
    send_key(VK_ESCAPE, KEYBD_EVENT_FLAGS(0))?;
    send_key(VK_ESCAPE, KEYBD_EVENT_FLAGS(2))?;

    Ok(())
}

fn is_windows_11() -> bool {
    // Windows 11 reports major version 10, build >= 22000
    let os = os_info::get();
    if os.os_type() == os_info::Type::Windows {
        if let Some(version) = os.version().to_string().split('.').nth(2) {
            return version
                .parse::<u32>()
                .map(|build| build >= 22000)
                .unwrap_or(false);
        }
    }
    // Fallback: check environment variable
    env::var("WINDOWS_BUILD")
        .ok()
        .and_then(|v| v.parse::<u32>().ok())
        .map(|build| build >= 22000)
        .unwrap_or(false)
}

/// Find a window by its class name.
/// Returns `Some(HWND)` if found, or `None` if not found.
pub fn find_window_by_class_name(class_name: &str) -> Option<HWND> {
    use windows::core::HSTRING;

    // Convert the class name to a wide string for FindWindowW
    let class_hstring = HSTRING::from(class_name);

    // Find the window with the given class name (passing null for window name)
    let hwnd = unsafe { FindWindowW(PCWSTR(class_hstring.as_ptr()), PCWSTR::null()) };

    if hwnd.0 != 0 { Some(hwnd) } else { None }
}

/// Gets the window handle of the eBIRForms application.
/// Returns None if the window can't be found.
pub fn get_ebir_window() -> Option<HWND> {
    // Try to find by class name first
    if let Some(hwnd) = find_window_by_class_name(EBIRFORMS_CLASS_NAME) {
        // Verify it's the right window by checking its visibility
        if unsafe { IsWindowVisible(hwnd) } == BOOL(1) {
            // Additional verification could be done here, like checking the window title
            return Some(hwnd);
        }
    }

    // If not found by class, fall back to process name
    find_hwnd_by_process_name(EBIRFORMS_PROCESS_NAME)
}

#[cfg(test)]
mod tests {
    // Commented tests need these imports
    #[allow(unused_imports)]
    use super::{find_hwnd_by_pid, open_ebir_window};
    use crate::workflows::type_tin;

    #[test]
    fn test_focus_window_by_hwnd() {
        if let Some(hwnd) = super::find_hwnd_by_process_name("mshta.exe") {
            assert!(super::focus_window_by_hwnd(hwnd));
        }
    }

    #[test]
    fn test_find_and_focus_window() {
        // open_ebir_window();
        // assert!(find_and_focus_window());
        open_ebir_window(None, None);
        // assert!(send_snap_shortcuts().is_ok());
    }

    #[test]
    fn test_find_process() {
        // find_hwnd_by_pid(6644);
        let handle = find_hwnd_by_pid(11872);
        println!("{:?}", handle);
    }

    #[test]
    fn test_find_hwnd_by_process_name() {
        let hwnd = super::find_hwnd_by_process_name("mshta.exe");
        println!("HWND: {:?}", hwnd);
    }

    // #[test]
    // fn test_open_ebir_and_type() {
    //     let hwnd = open_ebir_window(None, None);
    //     if let Some(hwnd) = hwnd {
    //         println!("HWND: {:?}", hwnd);
    //         type_tin("004", "185", "403", "000", hwnd);
    //     }
    // }
}
