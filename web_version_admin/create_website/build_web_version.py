#!/usr/bin/env python3
import json
import base64
import os
import shutil
import py_compile
import stat
import sys

# === CCRI Web Version Builder (Python Edition) ===

ENCODE_KEY = "CTF4EVER"

def abort(msg):
    print(f"❌ {msg}")
    sys.exit(1)

def xor_encode(plaintext, key):
    """XOR + Base64 encode a plaintext flag."""
    return base64.b64encode(
        bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(plaintext)])
    ).decode()

def make_scripts_executable(challenges_data, base_dir):
    """Set chmod +x on all helper scripts in challenges."""
    for meta in challenges_data.values():
        challenge_folder = os.path.join(base_dir, "challenges", os.path.basename(meta["folder"]))
        script_path = os.path.join(challenge_folder, meta["script"])
        if os.path.isfile(script_path):
            os.chmod(script_path, os.stat(script_path).st_mode | stat.S_IXUSR)
            print(f"✅ Made executable: {script_path}")
        else:
            print(f"⚠️ Skipping missing script: {script_path}")

def sanitize_templates(template_dir):
    """Replace admin hub text with dynamic mode handling."""
    print("📝 Sanitizing templates for student version...")
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                content = content.replace(
                    "CCRI CTF Admin Hub",
                    "{{ 'CCRI CTF Admin Hub' if mode == 'admin' else 'CCRI CTF Student Hub' }}"
                )
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Sanitized {path}")

def prepare_web_version(base_dir):
    admin_dir = os.path.join(base_dir, "web_version_admin")
    student_dir = os.path.join(base_dir, "web_version")
    admin_json = os.path.join(admin_dir, "challenges.json")
    templates_folder = os.path.join(admin_dir, "templates")
    static_folder = os.path.join(admin_dir, "static")
    server_source = os.path.join(admin_dir, "server.py")
    challenge_py = os.path.join(admin_dir, "Challenge.py")
    challenge_list_py = os.path.join(admin_dir, "ChallengeList.py")

    # === Validate admin folder contents ===
    print(f"📂 Using BASE_DIR: {base_dir}")
    if not os.path.isfile(admin_json):
        abort(f"Missing {admin_json}")
    if not os.path.isfile(server_source):
        abort(f"Missing {server_source}")
    if not os.path.isfile(challenge_py) or not os.path.isfile(challenge_list_py):
        abort("Missing Challenge.py or ChallengeList.py in admin folder")
    if not os.path.isdir(templates_folder):
        abort(f"Missing templates folder: {templates_folder}")
    if not os.path.isdir(static_folder):
        abort(f"Missing static folder: {static_folder}")

    # === Clean and recreate student web folder ===
    if os.path.exists(student_dir):
        print("🧹 Cleaning existing web_version folder...")
        shutil.rmtree(student_dir)
    os.makedirs(student_dir, exist_ok=True)

    # === Process challenges.json ===
    print("🔐 Encoding flags for student hub...")
    with open(admin_json, "r", encoding="utf-8") as f:
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
    make_scripts_executable(admin_data, base_dir)

    # === Write student challenges.json ===
    student_json_path = os.path.join(student_dir, "challenges.json")
    with open(student_json_path, "w", encoding="utf-8") as f:
        json.dump(student_data, f, indent=4)
    print(f"✅ Created {student_json_path}")

    # === Copy templates and static assets ===
    print("📂 Copying templates and static files...")
    shutil.copytree(templates_folder, os.path.join(student_dir, "templates"), dirs_exist_ok=True)
    shutil.copytree(static_folder, os.path.join(student_dir, "static"), dirs_exist_ok=True)

    # === Sanitize templates ===
    sanitize_templates(os.path.join(student_dir, "templates"))

    # === Compile backend .py files ===
    print("⚙️ Compiling backend Python files to .pyc...")
    py_compile.compile(server_source, cfile=os.path.join(student_dir, "server.pyc"))
    py_compile.compile(challenge_py, cfile=os.path.join(student_dir, "Challenge.pyc"))
    py_compile.compile(challenge_list_py, cfile=os.path.join(student_dir, "ChallengeList.pyc"))
    print("✅ Compiled backend .py files to .pyc in student folder")

    # === Write mode marker ===
    mode_file_path = os.path.join(student_dir, ".mode")
    with open(mode_file_path, "w", encoding="utf-8") as f:
        f.write("student\n")
    print(f"📄 Wrote mode marker: {mode_file_path}")

    print("\n🎉 Student web_version build completed successfully!\n")

def write_admin_mode_marker(base_dir):
    """Write admin mode marker for admin hub."""
    admin_mode_file = os.path.join(base_dir, ".mode")
    with open(admin_mode_file, "w", encoding="utf-8") as f:
        f.write("admin\n")
    print(f"📄 Wrote mode marker for admin site: {admin_mode_file}")

def main():
    print("🚀 Starting Web Version Build Process...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    prepare_web_version(base_dir)
    write_admin_mode_marker(base_dir)
    print("✅ Build process finished successfully.")
    input("\n📖 Press ENTER to exit...")

if __name__ == "__main__":
    main()
