#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
import sys
import subprocess
import pwd
import re

# === Target solo-only destination on ccri_admin's desktop ===
target_user = "ccri_admin"
target_home = Path(f"/home/{target_user}")
target_desktop = target_home / "Desktop"
target_folder_name = "stemday_2025_solo"
target_root = target_desktop / target_folder_name

# === Current project folder ===
source_root = Path(__file__).resolve().parent

# === Items to copy (relative to source_root) ===
# Solo-only: no guided "challenges" folder, no ".mode"
include = [
    "challenges_solo",
    "web_version",
    "ccri_ctf.pyz",                 # ⬅️ add the student zipapp
    "start_web_hub.py",
    "stop_web_hub.py",
    "Launch_CCRI_CTF_HUB.desktop",
    ".ccri_ctf_root",
    "LICENSE",
]

def ensure_owner_perms(path: Path, uid: int, gid: int):
    def is_script(fname: str) -> bool:
        # Treat .pyz and .desktop as executables
        return fname.endswith((".py", ".sh", ".desktop", ".pyz"))

    def is_plain_text(fname: str) -> bool:
        return fname.endswith((".txt", ".md", ".json"))

    if path.is_dir():
        for dirpath, _, filenames in os.walk(path):
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
        os.chown(path, uid, gid)
        if is_script(path.name):
            os.chmod(path, 0o755)
        elif is_plain_text(path.name):
            os.chmod(path, 0o644)
        else:
            os.chmod(path, 0o644)

def patch_desktop_file(src: Path, dst: Path):
    """
    Rewrites the Exec= line to point at the solo folder and start_web_hub.py.
    Also normalizes Icon to a generic 'firefox' for cross-distro compatibility.
    """
    content = src.read_text(encoding="utf-8", errors="ignore")
    # Exec line → cd into solo folder then run launcher
    content = re.sub(
        r'^Exec=.*$',
        f'Exec=bash -c \'cd "$HOME/Desktop/{target_folder_name}" && python3 start_web_hub.py\'',
        content,
        flags=re.MULTILINE,
    )
    # Icon normalization (optional but helpful)
    if "Icon=" in content:
        content = re.sub(r'^Icon=.*$', 'Icon=firefox', content, flags=re.MULTILINE)
    else:
        if not content.endswith("\n"): content += "\n"
        content += "Icon=firefox\n"

    dst.write_text(content, encoding="utf-8")

def mark_launcher_trusted(launcher_path: Path):
    """Mark the .desktop file as trusted in Nemo/Cinnamon (Mint). Harmless if gio missing."""
    try:
        subprocess.run(
            ["gio", "set", str(launcher_path), "metadata::trusted", "true"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print("🔐 Marked launcher as trusted with gio metadata.")
    except Exception as e:
        print(f"ℹ️ Skipped gio trust (not available or failed): {e}")

def prune_web_version(dst_web: Path):
    """
    In the copied web_version:
      - remove challenges.json (guided)
      - keep challenges_solo.json
      - remove templates/challenge.html (guided detail page)
      - keep templates/challenge_solo.html
    """
    guided_json = dst_web / "challenges.json"
    if guided_json.exists():
        guided_json.unlink()
        print("🧹 Removed web_version/challenges.json")

    templates = dst_web / "templates"
    guided_tpl = templates / "challenge.html"
    if guided_tpl.exists():
        guided_tpl.unlink()
        print("🧹 Removed web_version/templates/challenge.html")

def copy_item(src: Path, dst: Path):
    """Copy src -> dst fresh (remove existing first)."""
    if dst.exists():
        if dst.is_dir() and src.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        # Patch the .desktop file so Exec points to the solo folder
        if src.name == "Launch_CCRI_CTF_HUB.desktop":
            patch_desktop_file(src, dst)
        else:
            shutil.copy2(src, dst)

def main():
    print(f"📂 Source: {source_root}")
    print(f"📥 Target: {target_root}")

    # Make sure target root exists but don't wipe it
    target_root.mkdir(parents=True, exist_ok=True)

    # Copy only the selected items
    for item in include:
        src = source_root / item
        dst = target_root / item
        if src.exists():
            print(f"➡️ Copying {item}...")
            copy_item(src, dst)
        else:
            print(f"⚠️ Skipping missing item: {item}")

    # Solo pruning in web_version
    dst_web = target_root / "web_version"
    if dst_web.exists():
        prune_web_version(dst_web)

    # Defensive: remove guided folder if it slipped in
    guided_dir = target_root / "challenges"
    if guided_dir.exists():
        shutil.rmtree(guided_dir, ignore_errors=True)
        print("🧹 Removed stray guided 'challenges/' folder")

    # Fix ownership and perms for everything under target_root
    uid = pwd.getpwnam(target_user).pw_uid
    gid = pwd.getpwnam(target_user).pw_gid
    ensure_owner_perms(target_root, uid, gid)

    # Ensure launcher is executable & trusted
    launcher = target_root / "Launch_CCRI_CTF_HUB.desktop"
    if launcher.exists():
        os.chmod(launcher, 0o755)
        os.chown(launcher, uid, gid)
        mark_launcher_trusted(launcher)
    else:
        print("⚠️ No desktop launcher found to trust.")

    print("\n✅ Solo-only bundle ready.")
    print(f"📎 Open: {target_root}")
    print("💡 Tip: run the app and visit http://127.0.0.1:5000/healthz to confirm modes.")

if __name__ == "__main__":
    main()
