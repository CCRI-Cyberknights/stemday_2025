#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import stat
import sys
import subprocess
import pwd
import grp

# === Target student user and desktop path ===
target_user = "ccri_stem"
target_group = "ccri_ctf"
target_home = Path(f"/home/{target_user}")
target_desktop = target_home / "Desktop"
target_folder_name = "stemday_2025"
target_root = target_desktop / target_folder_name

# === Current project folder ===
source_root = Path(__file__).resolve().parent

# === Items to copy (relative to source_root) ===
include = [
    "challenges",
    "challenges_solo",
    "web_version",
    "start_web_hub.py",
    "stop_web_hub.py",
    "Launch_CCRI_CTF_HUB.desktop",
    ".mode",
    ".ccri_ctf_root"
]

def copy_and_fix(src: Path, dst: Path):
    """Copy src to dst, replacing existing, then fix ownership and permissions."""
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

    uid = pwd.getpwnam(target_user).pw_uid
    gid = grp.getgrnam(target_group).gr_gid

    def is_script(fname):
        return fname.endswith((".py", ".sh", ".desktop"))

    def is_plain_text(fname):
        return fname.endswith((".txt", ".md", ".json"))

    # Apply ownership and permissions
    for dirpath, _, filenames in os.walk(dst) if dst.is_dir() else [(dst.parent, [], [dst.name])]:
        os.chown(dirpath, uid, gid)
        os.chmod(dirpath, 0o2775)

        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            os.chown(fpath, uid, gid)

            if is_script(fname):
                os.chmod(fpath, 0o775)
            elif is_plain_text(fname):
                os.chmod(fpath, 0o664)
            else:
                os.chmod(fpath, 0o664)

    # Top-level single file
    if dst.is_file():
        os.chown(dst, uid, gid)
        if is_script(dst.name):
            os.chmod(dst, 0o775)
        elif is_plain_text(dst.name):
            os.chmod(dst, 0o664)
        else:
            os.chmod(dst, 0o664)

def main():
    if os.geteuid() != 0:
        print("🛡️ Elevation required. Re-running with sudo...")
        try:
            subprocess.run(["sudo", "python3"] + sys.argv)
        except Exception as e:
            print(f"❌ Failed to elevate privileges: {e}")
        sys.exit(0)

    print(f"📂 Source: {source_root}")
    print(f"📥 Target: {target_root}")

    if target_root.exists():
        print(f"🗑️ Removing existing folder: {target_root}")
        shutil.rmtree(target_root)

    target_root.mkdir(parents=True, exist_ok=True)

    for item in include:
        src = source_root / item
        dst = target_root / item
        if src.exists():
            print(f"➡️ Copying {item}...")
            copy_and_fix(src, dst)
        else:
            print(f"⚠️ Skipping missing item: {item}")

    print("\n✅ Done. Content copied and ownership/permissions adjusted.")
    print(f"📎 Now accessible in: {target_root}")

if __name__ == "__main__":
    main()
