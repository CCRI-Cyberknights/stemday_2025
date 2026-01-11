#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import sys
import subprocess
import pwd
import re

# === Configuration ===
target_user = "ccri_admin"
target_folder_name = "stemday_2025_takehome"

# === Items to copy (relative to source_root) ===
include = [
    "challenges",
    "challenges_solo",
    "web_version",
    "ccri_ctf.pyz",                 # Student deliverable
    "start_web_hub.py",
    "stop_web_hub.py",
    ".ccri_ctf_root",               # Critical marker for exploration scripts
    "coach_core.py",                # Coach Mode Backend
    "worker_node.py",               # Coach Mode Worker
    "exploration_core.py",
    "reset_environment.py",
]

def copy_and_fix(src: Path, dst: Path, uid: int, gid: int):
    """Copy src to dst (replace if exists) and set ownership/perms."""
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

    # Ownership & permissions logic
    def is_script(fname: str) -> bool:
        return fname.endswith((".py", ".sh", ".desktop", ".pyz", ".command"))

    def is_plain_text(fname: str) -> bool:
        return fname.endswith((".txt", ".md", ".json", ".gitignore", ".log"))

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
                else:
                    os.chmod(fpath, 0o644)
    else:
        os.chown(dst, uid, gid)
        if is_script(dst.name):
            os.chmod(dst, 0o755)
        else:
            os.chmod(dst, 0o644)

def generate_desktop_launcher(launcher_dst: Path, uid: int, gid: int):
    """Generates the .desktop file specifically for the Take-Home path assumption."""
    
    # We assume the student puts the folder on their Desktop.
    # We use $HOME in the path so it works for any username.
    work_dir = f"$HOME/Desktop/{target_folder_name}"
    icon_path = f"{work_dir}/icon.png"
    
    content = (
        "[Desktop Entry]\n"
        "Version=1.0\n"
        "Type=Application\n"
        "Terminal=true\n"
        "Name=Launch CCRI CTF Hub (Take-Home)\n"
        f"Exec=bash -c 'cd \"{work_dir}\" && python3 start_web_hub.py'\n"
        f"Icon={icon_path}\n"
        "Name[en_US]=Launch CCRI CTF Hub (Take-Home)\n"
        "Comment=Start the CyberKnights Challenge Hub\n"
    )
    
    launcher_dst.write_text(content, encoding="utf-8")
    os.chown(launcher_dst, uid, gid)
    os.chmod(launcher_dst, 0o755)

def mark_launcher_trusted(launcher_path: Path):
    """Mark the .desktop file as trusted (Mint/Nemo) via gio."""
    try:
        subprocess.run(
            ["gio", "set", str(launcher_path), "metadata::trusted", "true"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("🔐 Marked launcher as trusted with gio metadata.")
    except Exception:
        pass

def main():
    source_root = Path(__file__).resolve().parent
    
    # Verify User
    try:
        uid = pwd.getpwnam(target_user).pw_uid
        gid = pwd.getpwnam(target_user).pw_gid
    except KeyError:
        print(f"❌ User {target_user} not found. Cannot populate their desktop.")
        sys.exit(1)

    target_home = Path(f"/home/{target_user}")
    target_desktop = target_home / "Desktop"
    target_root = target_desktop / target_folder_name

    print(f"📂 Source: {source_root}")
    print(f"📥 Target: {target_root}")

    # Ensure target root exists
    if not target_root.exists():
        target_root.mkdir(parents=True, exist_ok=True)
    
    # Set root permissions
    os.chown(target_root, uid, gid)
    os.chmod(target_root, 0o755)

    # Check for marker
    marker = source_root / ".ccri_ctf_root"
    if not marker.exists():
        print("⚠️ Marker .ccri_ctf_root missing in source. Creating it...")
        marker.touch()

    # Copy Items
    for item in include:
        src = source_root / item
        dst = target_root / item
        if src.exists():
            print(f"➡️ Copying {item}...")
            copy_and_fix(src, dst, uid, gid)
        else:
            print(f"⚠️ Skipping missing item: {item}")

    # Copy Custom Icon
    icon_src = source_root / "web_version_admin" / "static" / "assets" / "CyberKnights_2.png"
    icon_dst = target_root / "icon.png"
    if icon_src.exists():
        print("🎨 Copying custom icon...")
        shutil.copy2(icon_src, icon_dst)
        os.chown(icon_dst, uid, gid)
        os.chmod(icon_dst, 0o644)

    # Generate Launcher inside the folder
    launcher = target_root / "Launch_CCRI_CTF_HUB.desktop"
    print("📎 Generating portable launcher...")
    generate_desktop_launcher(launcher, uid, gid)
    mark_launcher_trusted(launcher)

    print("\n✅ Done. Take-home version populated.")
    print(f"📎 Location: {target_root}")
    print("ℹ️  Instructions: Zip this folder and distribute it. Students should extract it to their Desktop.")

if __name__ == "__main__":
    main()