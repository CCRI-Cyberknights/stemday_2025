#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import stat
import sys
import subprocess
import pwd
import grp

# === Target take-home destination on ccri_admin's desktop ===
target_user = "ccri_admin"
target_home = Path(f"/home/{target_user}")
target_desktop = target_home / "Desktop"
target_folder_name = "stemday_2025_takehome"
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
    """Copy src to dst, replacing existing file/folder, then fix ownership and permissions."""
    if dst.exists():
        if dst.is_dir() and src.is_dir():
            shutil.rmtree(dst)
        elif dst.is_file():
            dst.unlink()

    if src.is_dir():
        shutil.copytree(src, dst)
    elif src.name == "Launch_CCRI_CTF_HUB.desktop":
        # Patch .desktop path reference before copying
        content = src.read_text(encoding="utf-8")
        patched = content.replace(
            "~/Desktop/stemday_2025/",
            "~/Desktop/stemday_2025_takehome/"
        )
        dst.write_text(patched, encoding="utf-8")
    else:
        shutil.copy2(src, dst)

    # Fix ownership and permissions
    uid = pwd.getpwnam(target_user).pw_uid
    gid = pwd.getpwnam(target_user).pw_gid

    def is_script(fname):
        return fname.endswith((".py", ".sh", ".desktop"))

    def is_plain_text(fname):
        return fname.endswith((".txt", ".md", ".json"))

    if dst.is_dir():
        for dirpath, _, filenames in os.walk(dst):
            os.chown(dirpath, uid, gid)
            os.chmod(dirpath, 0o755)
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                os.chown(fpath, uid, gid)
                if is_script(fname):
                    os.chmod(fpath, 0o755)
                elif is_plain_text(fname):
                    os.chmod(fpath, 0o644)
                else:
                    os.chmod(fpath, 0o644)
    else:
        os.chown(dst, uid, gid)
        if is_script(dst.name):
            os.chmod(dst, 0o755)
        elif is_plain_text(dst.name):
            os.chmod(dst, 0o644)
        else:
            os.chmod(dst, 0o644)

def main():
    print(f"📂 Source: {source_root}")
    print(f"📥 Target: {target_root}")

    # Make sure target root exists but don't wipe it
    target_root.mkdir(parents=True, exist_ok=True)

    for item in include:
        src = source_root / item
        dst = target_root / item
        if src.exists():
            print(f"➡️ Copying {item}...")
            copy_and_fix(src, dst)
        else:
            print(f"⚠️ Skipping missing item: {item}")

    print("\n✅ Done. Take-home version populated.")
    print(f"📎 Check: {target_root}")

if __name__ == "__main__":
    main()
