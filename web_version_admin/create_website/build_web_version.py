#!/usr/bin/env python3
import json
import base64
import os
import shutil
import py_compile
import stat
import sys

# === CCRI Web Version Builder (Dual Setup Edition) ===

ENCODE_KEY = "CTF4EVER"

def abort(msg):
    print(f"❌ {msg}")
    sys.exit(1)

def xor_encode(plaintext: str, key: str) -> str:
    """XOR + Base64 encode a plaintext flag."""
    return base64.b64encode(
        bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(plaintext)])
    ).decode()

def make_scripts_executable(challenges_data, base_dir):
    """Set chmod +x on all helper scripts in challenges (if present)."""
    for meta in challenges_data.values():
        script = meta.get("script")
        if not script:
            continue
        challenge_folder = os.path.join(base_dir, "challenges", os.path.basename(meta["folder"]))
        script_path = os.path.join(challenge_folder, script)
        if os.path.isfile(script_path):
            os.chmod(script_path, os.stat(script_path).st_mode | stat.S_IXUSR)
            print(f"✅ Made executable: {script_path}")
        else:
            print(f"⚠️ Skipping missing script: {script_path}")

def sanitize_templates(template_dir):
    """Replace Admin Hub text with dynamic mode handling."""
    print("📝 Sanitizing templates for student version...")
    for root, _, files in os.walk(template_dir):
        for file in files:
            if not file.endswith(".html"):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Use dynamic title for student/admin
            content = content.replace(
                "CCRI CTF Admin Hub",
                "{{ 'CCRI CTF Admin Hub' if base_mode == 'admin' else 'CCRI CTF Student Hub' }}"
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Sanitized {path}")

def _looks_base64(s: str) -> bool:
    try:
        base64.b64decode(s.encode(), validate=True)
        return True
    except Exception:
        return False

def prepare_web_version(base_dir):
    admin_dir = os.path.join(base_dir, "web_version_admin")
    student_dir = os.path.join(base_dir, "web_version")
    admin_json = os.path.join(admin_dir, "challenges.json")
    solo_json = os.path.join(admin_dir, "challenges_solo.json")
    templates_folder = os.path.join(admin_dir, "templates")
    static_folder = os.path.join(admin_dir, "static")
    server_source = os.path.join(admin_dir, "server.py")
    challenge_py = os.path.join(admin_dir, "Challenge.py")
    challenge_list_py = os.path.join(admin_dir, "ChallengeList.py")

    # === Validate admin folder contents ===
    print(f"📂 Using BASE_DIR: {base_dir}")
    for p in (admin_json, solo_json, server_source, challenge_py, challenge_list_py):
        if not os.path.isfile(p):
            abort(f"Missing required file: {p}")
    for d in (templates_folder, static_folder):
        if not os.path.isdir(d):
            abort(f"Missing required folder: {d}")

    # === Clean and recreate student web folder ===
    if os.path.exists(student_dir):
        print("🧹 Cleaning existing web_version folder...")
        shutil.rmtree(student_dir)
    os.makedirs(student_dir, exist_ok=True)

    # === Process challenges.json (GUIDED) ===
    print("🔐 Encoding flags for student hub (Guided)...")
    with open(admin_json, "r", encoding="utf-8") as f:
        admin_data = json.load(f)

    guided_data = {}
    for cid, meta in admin_data.items():
        entry = {
            "name": meta["name"],
            "folder": meta["folder"],
            "flag": xor_encode(meta["flag"], ENCODE_KEY),
        }
        if meta.get("script"):
            entry["script"] = meta["script"]
        guided_data[cid] = entry

    # Make helper scripts executable for guided (if present)
    make_scripts_executable(admin_data, base_dir)

    guided_json_path = os.path.join(student_dir, "challenges.json")
    with open(guided_json_path, "w", encoding="utf-8") as f:
        json.dump(guided_data, f, indent=4, ensure_ascii=False)
    print(f"✅ Created Guided: {guided_json_path}")

    # === Process challenges_solo.json (SOLO) ===
    print("🔐 Encoding flags for student hub (Solo)...")
    with open(solo_json, "r", encoding="utf-8") as f:
        admin_solo = json.load(f)

    solo_data = {}
    for cid, meta in admin_solo.items():
        raw_flag = meta.get("real_flag", meta.get("flag"))
        if not raw_flag:
            abort(f"Solo entry {cid} has no flag/real_flag")
        entry = {
            "name": meta["name"],
            "folder": meta["folder"],
            "flag": xor_encode(raw_flag, ENCODE_KEY),
        }
        # Only include a script for solo if you explicitly ship one
        if meta.get("script"):
            entry["script"] = meta["script"]
        # Keep a mild hint if present (optional)
        if "hint" in meta:
            entry["hint"] = meta["hint"]
        solo_data[cid] = entry

    solo_json_path = os.path.join(student_dir, "challenges_solo.json")
    with open(solo_json_path, "w", encoding="utf-8") as f:
        json.dump(solo_data, f, indent=4, ensure_ascii=False)
    print(f"✅ Created Solo: {solo_json_path}")

    # === Verify encoding sanity (optional but helpful) ===
    for path in (guided_json_path, solo_json_path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        bad = [cid for cid, m in data.items() if not _looks_base64(m.get("flag", ""))]
        if bad:
            abort(f"Non-encoded flags found in {os.path.basename(path)}: {bad}")
        print(f"🔎 Verified encoding in {os.path.basename(path)}")

    # === Copy templates and static assets ===
    print("📂 Copying templates and static files...")
    shutil.copytree(templates_folder, os.path.join(student_dir, "templates"), dirs_exist_ok=True)
    shutil.copytree(static_folder, os.path.join(student_dir, "static"), dirs_exist_ok=True)

    # === Sanitize templates ===
    sanitize_templates(os.path.join(student_dir, "templates"))

    # === Compile backend .py files ===
    print("⚙️ Compiling backend Python files to .pyc...")
    py_compile.compile(server_source, cfile=os.path.join(student_dir, "server.pyc"), optimize=1)
    py_compile.compile(challenge_py, cfile=os.path.join(student_dir, "Challenge.pyc"), optimize=1)
    py_compile.compile(challenge_list_py, cfile=os.path.join(student_dir, "ChallengeList.pyc"), optimize=1)
    print("✅ Compiled backend .py files to .pyc in student folder")

    print("\n🎉 Student web_version build completed successfully!\n")

def main():
    print("🚀 Starting Web Version Build Process...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    prepare_web_version(base_dir)
    print("✅ Build process finished successfully.")
    input("\n📖 Press ENTER to exit...")

if __name__ == "__main__":
    main()
