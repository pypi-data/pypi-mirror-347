// Contains automations IDs, control names etc.

// Automation IDs for TIN fields
pub const TIN1_ID: &str = "tin1";
pub const TIN2_ID: &str = "tin2";
pub const TIN3_ID: &str = "tin3";
pub const TIN4_ID: &str = "tin4";

// eBIRForms application specific constants
pub const EBIRFORMS_PROCESS_NAME: &str = "mshta.exe";
pub const EBIRFORMS_CLASS_NAME: &str = "HTA";
#[allow(dead_code)]
pub const EBIRFORMS_WINDOW_TITLE_PARTIAL: &str = "eBIRForms";

// Virtual key codes
pub const VK_LWIN: u16 = 0x5B;
pub const VK_Z: u16 = 0x5A;
pub const VK_1: u16 = 0x31;
pub const VK_ESCAPE: u16 = 0x1B;

// Default application path and snap key delay
pub const DEFAULT_APP_PATH: &str = r"C:\eBIRForms\BIRForms.exe";
pub const SNAP_KEY_DELAY: std::time::Duration = std::time::Duration::from_millis(500);
