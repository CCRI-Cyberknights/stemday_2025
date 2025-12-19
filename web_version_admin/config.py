import os
import sys

# ---------- PATH RESOLUTION ----------
ASSETS_DIR_OVERRIDE = os.environ.get("CCRI_ASSETS_DIR")

def detect_assets_dir():
    """
    Priority:
      1) CCRI_ASSETS_DIR (env)
      2) <dir_of_running_pyz>/web_version (next to the pyz)
      3) directory of this source file (dev/admin tree)
    """
    if ASSETS_DIR_OVERRIDE:
        return os.path.abspath(ASSETS_DIR_OVERRIDE)

    pyz_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    candidate = os.path.join(pyz_dir, "web_version")
    if os.path.isdir(candidate):
        return candidate

    return os.path.dirname(os.path.abspath(__file__))

server_dir = detect_assets_dir()
BASE_DIR   = os.path.abspath(os.path.join(server_dir, ".."))
template_folder = os.path.join(server_dir, "templates")
static_folder   = os.path.join(server_dir, "static")

# ---------- MODE CONFIGURATION ----------
DEBUG_MODE = os.environ.get("CCRI_DEBUG", "0") == "1"

# Base Mode: Admin vs Student
base_mode = os.environ.get("CCRI_CTF_MODE", "").strip().lower()
if not base_mode:
    base_mode = "admin" if os.path.basename(server_dir) == "web_version_admin" else "student"

has_admin = os.path.isdir(os.path.join(BASE_DIR, "web_version_admin"))
if base_mode == "admin" and not has_admin:
    print("⚠️ Admin mode requested but admin assets missing; forcing STUDENT mode.")
    base_mode = "student"

os.environ["CCRI_CTF_MODE"] = base_mode

# Folders containing challenge data
GUIDED_DIR = os.path.join(BASE_DIR, "challenges")
SOLO_DIR   = os.path.join(BASE_DIR, "challenges_solo")

def detect_available_modes():
    modes = []
    if os.path.isdir(GUIDED_DIR):
        modes.append("regular")
    if os.path.isdir(SOLO_DIR):
        modes.append("solo")
    return modes

AVAILABLE_MODES = detect_available_modes()
DEFAULT_MODE = "regular" if "regular" in AVAILABLE_MODES else ("solo" if "solo" in AVAILABLE_MODES else None)