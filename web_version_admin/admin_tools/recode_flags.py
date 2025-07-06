import json
import base64
import os
import shutil
import py_compile
import stat

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
        # Fix folder path resolution
        relative_folder = meta["folder"].lstrip("./").lstrip("../")
        folder = os.path.join(BASE_DIR, relative_folder)
        script_path = os.path.join(folder, meta["script"])
        if os.path.exists(script_path):
            current_mode = os.stat(script_path).st_mode
            os.chmod(script_path, current_mode | stat.S_IXUSR)
            print(f"✅ Made executable: {script_path}")
        else:
            print(f"⚠️ Script not found: {script_path}")

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

    # Copy templates & static files (allow overwrite if folder exists)
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

    # Compile server.py to server.pyc
    print("⚙️ Compiling server.py for student version...")
    compiled_path = os.path.join(STUDENT_DIR, "server.pyc")
    py_compile.compile(SERVER_SOURCE, cfile=compiled_path)
    print(f"✅ Compiled server saved as {compiled_path}")

    print("\n🎉 Student web_version folder rebuilt successfully!\n")

if __name__ == "__main__":
    print(f"📂 Detected BASE_DIR: {BASE_DIR}")
    prepare_web_version()
