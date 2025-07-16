#!/bin/bash

# === Bash Wrapper for Web Version Builder ===
echo "🚀 Starting Web Version Build Process..."

# === Check for PyInstaller ===
if ! command -v pyinstaller >/dev/null 2>&1; then
    echo "❌ PyInstaller is not installed. Install it with: sudo apt install pyinstaller"
    exit 1
fi

# === Display PyInstaller Version ===
PYI_VERSION=$(pyinstaller --version 2>/dev/null || echo "unknown")
echo "📦 Detected PyInstaller version: $PYI_VERSION"

# === Use Python3 to execute the embedded script ===
/usr/bin/env python3 <<'EOF'
import json
import base64
import os
import shutil
import subprocess
import stat
import sys

# === Dynamic Base Directory Detection ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ADMIN_DIR = os.path.join(BASE_DIR, "web_version_admin")
STUDENT_DIR = os.path.join(BASE_DIR, "web_version")

ADMIN_JSON = os.path.join(ADMIN_DIR, "challenges.json")
TEMPLATES_FOLDER = os.path.join(ADMIN_DIR, "templates")
STATIC_FOLDER = os.path.join(ADMIN_DIR, "static")
SERVER_SOURCE = os.path.join(ADMIN_DIR, "server.py")
ENCODE_KEY = "CTF4EVER"

def xor_encode(plaintext, key):
    """XOR + Base64 encode a plaintext flag."""
    encoded_bytes = bytes(
        [ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(plaintext)]
    )
    return base64.b64encode(encoded_bytes).decode()

def make_scripts_executable(challenges_data):
    """Set chmod +x on all helper scripts in the student folder"""
    for meta in challenges_data.values():
        relative_folder = meta["folder"].lstrip("./").lstrip("../")
        folder = os.path.join(BASE_DIR, relative_folder)
        script_path = os.path.join(folder, meta["script"])
        if os.path.exists(script_path):
            current_mode = os.stat(script_path).st_mode
            os.chmod(script_path, current_mode | stat.S_IXUSR)
            print(f"✅ Made executable: {script_path}")
        else:
            print(f"⚠️ Script not found: {script_path}")

def compile_server_binary():
    """Use PyInstaller to create a single-file binary of server.py"""
    print("⚙️ Compiling server.py with PyInstaller...")

    result = subprocess.run(
        ["pyinstaller", "--onefile", "--distpath", STUDENT_DIR, SERVER_SOURCE],
        cwd=ADMIN_DIR,  # Force PyInstaller to run from ADMIN_DIR
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print("❌ PyInstaller failed:")
        print(result.stderr)
        exit(1)

    print(f"✅ Compiled binary placed in {STUDENT_DIR}")

    # Clean up build artifacts
    for artifact in ["build", "server.spec", "__pycache__"]:
        artifact_path = os.path.join(ADMIN_DIR, artifact)
        if os.path.isdir(artifact_path):
            shutil.rmtree(artifact_path, ignore_errors=True)
            print(f"🧹 Cleaned folder: {artifact_path}")
        elif os.path.isfile(artifact_path):
            os.remove(artifact_path)
            print(f"🧹 Removed file: {artifact_path}")

def prepare_web_version():
    # Clear the student web_version folder
    if os.path.exists(STUDENT_DIR):
        print("🧹 Clearing existing web_version folder...")
        shutil.rmtree(STUDENT_DIR)
    os.makedirs(STUDENT_DIR)

    # Load admin challenges.json and encode flags
    print("🔐 Encoding flags for student web hub...")
    with open(ADMIN_JSON, "r") as f:
        admin_data = json.load(f)

    student_data = {}
    for cid, meta in admin_data.items():
        student_data[cid] = {
            "name": meta["name"],
            "folder": meta["folder"].replace("CCRI_CTF/", ""),  # adjust path
            "script": meta["script"],
            "flag": xor_encode(meta["flag"], ENCODE_KEY)
        }

    # Make all scripts executable in student challenges
    print("🔧 Setting execute permissions on helper scripts...")
    make_scripts_executable(admin_data)

    # Write student challenges.json
    student_json_path = os.path.join(STUDENT_DIR, "challenges.json")
    with open(student_json_path, "w") as f:
        json.dump(student_data, f, indent=4)
    print(f"✅ Student challenges.json created at {student_json_path}")

    # Copy templates & static files
    print("📂 Copying templates and static assets...")
    shutil.copytree(
        TEMPLATES_FOLDER,
        os.path.join(STUDENT_DIR, "templates"),
        dirs_exist_ok=True
    )
    shutil.copytree(
        STATIC_FOLDER,
        os.path.join(STUDENT_DIR, "static"),
        dirs_exist_ok=True
    )

    # Compile server.py to standalone binary
    compile_server_binary()

    print("\n🎉 Student web_version folder rebuilt successfully!\n")

if __name__ == "__main__":
    print(f"📂 Detected BASE_DIR: {BASE_DIR}")
    prepare_web_version()
EOF

echo "✅ Build process finished."

# Pause to review output
echo
read -p "📖 Press ENTER to exit..."
