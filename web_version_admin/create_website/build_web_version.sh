#!/bin/bash

# === CCRI Web Version Builder ===
echo "🚀 Starting Web Version Build Process..."

# === Check dependencies ===
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 is not installed. Install it first."
    exit 1
fi

# === Execute Python build logic ===
/usr/bin/env python3 <<'EOF'
import json
import base64
import os
import shutil
import py_compile
import stat
import sys

# === Paths ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ADMIN_DIR = os.path.join(BASE_DIR, "web_version_admin")
STUDENT_DIR = os.path.join(BASE_DIR, "web_version")

ADMIN_JSON = os.path.join(ADMIN_DIR, "challenges.json")
TEMPLATES_FOLDER = os.path.join(ADMIN_DIR, "templates")
STATIC_FOLDER = os.path.join(ADMIN_DIR, "static")
SERVER_SOURCE = os.path.join(ADMIN_DIR, "server.py")
CHALLENGE_PY = os.path.join(ADMIN_DIR, "Challenge.py")
CHALLENGELIST_PY = os.path.join(ADMIN_DIR, "ChallengeList.py")
ENCODE_KEY = "CTF4EVER"

def abort(msg):
    print(f"❌ {msg}")
    sys.exit(1)

def xor_encode(plaintext, key):
    """XOR + Base64 encode a plaintext flag."""
    return base64.b64encode(
        bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(plaintext)])
    ).decode()

def make_scripts_executable(challenges_data):
    """Set chmod +x on all helper scripts in BASE_DIR/challenges."""
    for meta in challenges_data.values():
        challenge_folder = os.path.join(BASE_DIR, "challenges", os.path.basename(meta["folder"]))
        script_path = os.path.join(challenge_folder, meta["script"])
        if os.path.isfile(script_path):
            os.chmod(script_path, os.stat(script_path).st_mode | stat.S_IXUSR)
            print(f"✅ Made executable: {script_path}")
        else:
            print(f"⚠️ Skipping missing script: {script_path}")

def prepare_web_version():
    # === Validate admin folder contents ===
    if not os.path.isfile(ADMIN_JSON):
        abort(f"Missing {ADMIN_JSON}")
    if not os.path.isfile(SERVER_SOURCE):
        abort(f"Missing {SERVER_SOURCE}")
    if not os.path.isfile(CHALLENGE_PY) or not os.path.isfile(CHALLENGELIST_PY):
        abort("Missing Challenge.py or ChallengeList.py in admin folder")
    if not os.path.isdir(TEMPLATES_FOLDER):
        abort(f"Missing templates folder: {TEMPLATES_FOLDER}")
    if not os.path.isdir(STATIC_FOLDER):
        abort(f"Missing static folder: {STATIC_FOLDER}")

    # === Clean and recreate student web folder ===
    if os.path.exists(STUDENT_DIR):
        print("🧹 Cleaning existing web_version folder...")
        shutil.rmtree(STUDENT_DIR)
    os.makedirs(STUDENT_DIR, exist_ok=True)

    # === Process challenges.json ===
    print("🔐 Encoding flags for student hub...")
    with open(ADMIN_JSON, "r", encoding="utf-8") as f:
        admin_data = json.load(f)

    student_data = {}
    for cid, meta in admin_data.items():
        student_data[cid] = {
            "name": meta["name"],
            "folder": meta["folder"],  # leave path unchanged
            "script": meta["script"],
            "flag": xor_encode(meta["flag"], ENCODE_KEY)
        }

    # === Make helper scripts executable ===
    make_scripts_executable(admin_data)

    # === Write student challenges.json ===
    student_json_path = os.path.join(STUDENT_DIR, "challenges.json")
    with open(student_json_path, "w", encoding="utf-8") as f:
        json.dump(student_data, f, indent=4)
    print(f"✅ Created {student_json_path}")

    # === Copy templates and static assets ===
    print("📂 Copying templates and static files...")
    shutil.copytree(TEMPLATES_FOLDER, os.path.join(STUDENT_DIR, "templates"), dirs_exist_ok=True)
    shutil.copytree(STATIC_FOLDER, os.path.join(STUDENT_DIR, "static"), dirs_exist_ok=True)

    # === Compile backend .py files ===
    print("⚙️ Compiling backend Python files to .pyc...")
    py_compile.compile(SERVER_SOURCE, cfile=os.path.join(STUDENT_DIR, "server.pyc"))
    py_compile.compile(CHALLENGE_PY, cfile=os.path.join(STUDENT_DIR, "Challenge.pyc"))
    py_compile.compile(CHALLENGELIST_PY, cfile=os.path.join(STUDENT_DIR, "ChallengeList.pyc"))
    print("✅ Compiled backend .py files to .pyc in student folder")

    # === Write mode marker ===
    mode_file_path = os.path.join(STUDENT_DIR, ".mode")
    with open(mode_file_path, "w", encoding="utf-8") as f:
        f.write("student\n")
    print(f"📄 Wrote mode marker: {mode_file_path}")

    print("\n🎉 Student web_version build completed successfully!\n")

# === Main Execution ===
print(f"📂 Using BASE_DIR: {BASE_DIR}")
prepare_web_version()
EOF

# === Write mode marker for admin site ===
echo "admin" > "$(dirname "$0")/../.mode"
echo "📄 Wrote mode marker for admin site"

echo "✅ Build process finished successfully."

# === Optional pause for review ===
echo
read -p "📖 Press ENTER to exit..."
