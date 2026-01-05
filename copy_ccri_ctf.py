#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import sys
import subprocess
import pwd
import grp
import re

def ensure_group_and_members(group_name, users):
    """Create group if missing, and ensure listed users are members."""
    try:
        group = grp.getgrnam(group_name)
        print(f"✅ Group '{group_name}' already exists.")
    except KeyError:
        print(f"➕ Group '{group_name}' not found. Creating it...")
        subprocess.run(["groupadd", group_name], check=True)
        group = grp.getgrnam(group_name)

    current_members = set(group.gr_mem)
    for user in users:
        if user and user not in current_members:
            print(f"👥 Adding '{user}' to group '{group_name}'...")
            subprocess.run(["usermod", "-aG", group_name, user], check=True)
        else:
            print(f"✅ User '{user}' is already in group '{group_name}'.")
    return group.gr_gid

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
    "ccri_ctf.pyz",        # student deliverable
    "start_web_hub.py",
    "stop_web_hub.py",
    ".ccri_ctf_root",
    "coach_core.py",       # ⬅️ NEW: Coach Mode Backend
    "worker_node.py",      # ⬅️ NEW: Coach Mode Worker
    "exploration_core.py",
    "reset_environment.py",
]

def copy_and_fix(src: Path, dst: Path, uid: int, gid: int):
    """Copy src to dst, replacing existing, then fix ownership and permissions."""
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    if src.is_dir():
        shutil.copytree(src, dst)  # permissions are normalized below
    else:
        shutil.copy2(src, dst)

    def is_script(fname):
        return fname.endswith((".py", ".sh", ".desktop", ".pyz"))

    def is_plain_text(fname):
        return fname.endswith((".txt", ".md", ".json"))

    if dst.is_dir():
        for dirpath, _, filenames in os.walk(dst):
            os.chown(dirpath, uid, gid)
            os.chmod(dirpath, 0o2775)  # rwx for owner/group; setgid
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                try:
                    os.chown(fpath, uid, gid)
                except FileNotFoundError:
                    continue
                if is_script(fname):
                    os.chmod(fpath, 0o775)
                elif is_plain_text(fname):
                    os.chmod(fpath, 0o664)
                else:
                    os.chmod(fpath, 0o664)
    else:
        os.chown(dst, uid, gid)
        if is_script(dst.name):
            os.chmod(dst, 0o775)
        elif is_plain_text(dst.name):
            os.chmod(dst, 0o664)
        else:
            os.chmod(dst, 0o664)

def write_or_patch_desktop_launcher(launcher_dst: Path, uid: int, gid: int):
    """Ensure the .desktop launcher exists and points to start_web_hub.py."""
    desired_exec = 'Exec=bash -c "cd $HOME/Desktop/stemday_2025 && python3 start_web_hub.py"'
    template = (
        "[Desktop Entry]\n"
        "Version=1.0\n"
        "Type=Application\n"
        "Terminal=true\n"
        "Name=Launch_CCRI_CTF_Hub\n"
        f"{desired_exec}\n"
        "Icon=utilities-terminal\n"
        "Name[en_US]=Launch_CCRI_CTF_Hub\n"
    )

    if launcher_dst.exists():
        try:
            text = launcher_dst.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            text = ""
        if "Exec=" in text:
            text = re.sub(r"^Exec=.*$", desired_exec, text, flags=re.MULTILINE)
        else:
            text = (text + ("\n" if not text.endswith("\n") else "")) + desired_exec + "\n"
    else:
        text = template

    launcher_dst.write_text(text, encoding="utf-8")
    os.chown(launcher_dst, uid, gid)
    os.chmod(launcher_dst, 0o775)

    # Mark as trusted in Nemo/Cinnamon (Mint); harmless elsewhere
    try:
        subprocess.run(
            ["gio", "set", str(launcher_dst), "metadata::trusted", "true"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("🔐 Marked launcher as trusted with gio metadata.")
    except Exception as e:
        print(f"ℹ️ Skipped gio trust (not available or failed): {e}")

def fix_tree_owner_perms(root: Path, uid: int, gid: int):
    """Final sweep to ensure everything under root (including root) has correct owner/perms."""
    for dirpath, dirnames, filenames in os.walk(root):
        os.chown(dirpath, uid, gid)
        os.chmod(dirpath, 0o2775)
        for name in filenames:
            p = os.path.join(dirpath, name)
            try:
                os.chown(p, uid, gid)
            except FileNotFoundError:
                continue
            # keep file modes as set earlier; don’t overwrite here

def main():
    # NEW: make group-writable defaults (so copies land 775/664 when we chmod)
    old_umask = os.umask(0o002)  # NEW

    if os.geteuid() != 0:
        print("🛡️ Elevation required. Re-running with sudo...")
        try:
            subprocess.run(["sudo", "python3"] + sys.argv, check=True)
        except Exception as e:
            print(f"❌ Failed to elevate privileges: {e}")
        sys.exit(0)

    invoking_user = os.environ.get("SUDO_USER")
    if not invoking_user:
        print("❌ Could not determine invoking user via SUDO_USER.")
        sys.exit(1)

    uid = pwd.getpwnam(target_user).pw_uid
    gid = ensure_group_and_members(target_group, [target_user, invoking_user])

    print(f"📂 Source: {source_root}")
    print(f"📥 Target: {target_root}")

    # Ensure target Desktop exists and is owned by the student
    if not target_desktop.exists():
        target_desktop.mkdir(parents=True, exist_ok=True)
        os.chown(target_desktop, uid, gid)
        os.chmod(target_desktop, 0o755)

    if target_root.exists():
        print(f"🗑️ Removing existing folder: {target_root}")
        shutil.rmtree(target_root)

    # Create the top-level folder and FIX ITS OWNER/PERMS RIGHT AWAY (IMPORTANT)
    target_root.mkdir(parents=True, exist_ok=True)
    os.chown(target_root, uid, gid)             # UPDATED (fix “locked”)
    os.chmod(target_root, 0o2775)               # UPDATED (group write + setgid)

    # Copy selected items
    for item in include:
        src = source_root / item
        dst = target_root / item
        if src.exists():
            print(f"➡️ Copying {item}...")
            copy_and_fix(src, dst, uid, gid)
        else:
            print(f"⚠️ Skipping missing item: {item}")

    # Desktop launcher
    launcher_dst = target_desktop / "Launch_CCRI_CTF_HUB.desktop"
    print("📎 Ensuring desktop launcher...")
    write_or_patch_desktop_launcher(launcher_dst, uid, gid)

    # FINAL SWEEP to catch anything missed (e.g., empty dirs, race conditions)
    fix_tree_owner_perms(target_root, uid, gid)  # NEW

    print("\n✅ Done. Content copied and ownership/permissions adjusted.")
    print(f"📎 Now accessible in: {target_root}")
    print("ℹ️ If you just added users to a group, log out and back in to apply membership.")

    os.umask(old_umask)  # restore

if __name__ == "__main__":
    main()