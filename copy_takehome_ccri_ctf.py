#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import sys
import subprocess
import pwd
import re

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
    "ccri_ctf.pyz",                 # ⬅️ NEW: student deliverable
    "start_web_hub.py",
    "stop_web_hub.py",
    "Launch_CCRI_CTF_HUB.desktop",
    ".mode",
    ".ccri_ctf_root",
    "coach_core.py",    # ⬅️ NEW: Coach Mode Backend
    "worker_node.py",   # ⬅️ NEW: Coach Mode Worker
    "exploration_core.py",
    "reset_environment.py",
]

def copy_and_fix(src: Path, dst: Path, uid: int, gid: int):
    """Copy src to dst (replace if exists) and set ownership/perms."""
    if dst.exists():
        if dst.is_dir() and src.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    # Special-case: patch the desktop shortcut before writing
    if src.name == "Launch_CCRI_CTF_HUB.desktop":
        content = src.read_text(encoding="utf-8", errors="ignore")

        # Normalize any previous folder reference → *_takehome
        content = re.sub(
            r'(?P<prefix>(~|\$HOME|\${HOME}|/home/[^/]+))/Desktop/stemday_2025(?P<trail>(/|\b))',
            r'\g<prefix>/Desktop/stemday_2025_takehome\g<trail>',
            content
        )

        # Force Exec line to run our launcher in the take-home dir
        content = re.sub(
            r'^Exec=.*$',
            'Exec=bash -c \'cd "$HOME/Desktop/stemday_2025_takehome" && python3 start_web_hub.py\'',
            content,
            flags=re.MULTILINE
        )

        # Prefer a generic icon so it works on Mint & Parrot alike
        content = re.sub(
            r'^Icon=.*$',
            'Icon=firefox',
            content,
            flags=re.MULTILINE
        )

        dst.write_text(content, encoding="utf-8")
    else:
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    # Ownership & permissions
    def is_script(fname: str) -> bool:
        # Treat .pyz and .desktop as executables
        return fname.endswith((".py", ".sh", ".desktop", ".pyz"))

    def is_plain_text(fname: str) -> bool:
        return fname.endswith((".txt", ".md", ".json", ".gitignore"))

    if dst.is_dir():
        for dirpath, _, filenames in os.walk(dst):
            os.chown(dirpath, uid, gid)
            os.chmod(dirpath, 0o755)
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                try:
                    os.chown(fpath, uid, gid)
                except FileNotFoundError:
                    continue
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

def mark_launcher_trusted(launcher_path: Path):
    """Mark the .desktop file as trusted (Mint/Nemo) via gio; safe to skip if not present."""
    try:
        subprocess.run(
            ["gio", "set", str(launcher_path), "metadata::trusted", "true"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("🔐 Marked launcher as trusted with gio metadata.")
    except Exception as e:
        print(f"ℹ️ Skipped gio trust (not available or failed): {e}")

def main():
    print(f"📂 Source: {source_root}")
    print(f"📥 Target: {target_root}")

    # Ensure target root exists (don't wipe the whole folder automatically for take-home)
    target_root.mkdir(parents=True, exist_ok=True)

    uid = pwd.getpwnam(target_user).pw_uid
    gid = pwd.getpwnam(target_user).pw_gid

    for item in include:
        src = source_root / item
        dst = target_root / item
        if src.exists():
            print(f"➡️ Copying {item}...")
            copy_and_fix(src, dst, uid, gid)
        else:
            print(f"⚠️ Skipping missing item: {item}")

    # Ensure .desktop is executable & trusted
    launcher = target_root / "Launch_CCRI_CTF_HUB.desktop"
    if launcher.exists():
        os.chmod(launcher, 0o755)
        os.chown(launcher, uid, gid)
        mark_launcher_trusted(launcher)
    else:
        print("⚠️ No desktop launcher found to trust.")

    print("\n✅ Done. Take-home version populated.")
    print(f"📎 Check: {target_root}")

if __name__ == "__main__":
    main()