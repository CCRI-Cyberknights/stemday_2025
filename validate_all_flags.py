#!/usr/bin/env python3
import subprocess
import shutil
import sys
import os
import json
from pathlib import Path

# === CCRI STEMDay Master Validator ===
VALIDATION_ROOT = Path.cwd() / "validation_results"
CHALLENGES_ROOT = Path.cwd() / "challenges"
CHALLENGES_JSON = Path.cwd() / "web_version_admin" / "challenges.json"
CHALLENGES_ROOT_SOLO = Path.cwd() / "challenges_solo"
CHALLENGES_JSON_SOLO = Path.cwd() / "web_version_admin" / "challenges_solo.json"
UNLOCKS_GUIDED = Path.cwd() / "web_version_admin" / "validation_unlocks.json"
UNLOCKS_SOLO = Path.cwd() / "web_version_admin" / "validation_unlocks_solo.json"

HELPER_TIMEOUT = 30
VERBOSE = False

def log_verbose(message):
    if VERBOSE:
        print(f"📝 [VERBOSE] {message}")

def clean_validation_folder():
    if VALIDATION_ROOT.exists():
        print("🧹 Cleaning old validation_results...")
        shutil.rmtree(VALIDATION_ROOT)
    VALIDATION_ROOT.mkdir()
    print("📁 Created fresh validation_results/ folder.")

def load_challenges_json(mode):
    json_path = CHALLENGES_JSON_SOLO if mode == "solo" else CHALLENGES_JSON
    if not json_path.exists():
        print(f"❌ ERROR: {json_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_guided_scripts():
    if not CHALLENGES_JSON.exists():
        return {}
    with open(CHALLENGES_JSON, "r", encoding="utf-8") as f:
        return {k: v.get("script") for k, v in json.load(f).items()}

def load_validation_unlocks(mode):
    unlocks_file = UNLOCKS_SOLO if mode == "solo" else UNLOCKS_GUIDED
    if not unlocks_file.exists():
        print(f"❌ ERROR: {unlocks_file} not found.", file=sys.stderr)
        sys.exit(1)
    with open(unlocks_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for entry in data.values():
            for field in ("vigenere_key", "last_password", "zip_password"):
                if field in entry and isinstance(entry[field], str):
                    entry[field] = entry[field].lower()
        return data

def validate_challenge(challenge_id, entry, timeouts, base_folder, mode, fallback_scripts):
    print(f"\n🔍 Validating {challenge_id}: {entry['name']}...")
    original_folder = base_folder / entry["folder"]
    validation_folder = VALIDATION_ROOT / entry["folder"]
    validation_folder.mkdir(parents=True, exist_ok=True)

    for item in original_folder.iterdir():
        dest = validation_folder / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    script_name = entry.get("script") or fallback_scripts.get(challenge_id)
    if not script_name:
        print(f"⚠️ Skipping {challenge_id}: No helper script defined.")
        return False

    script_path = validation_folder / script_name

    # ✅ Fallback: if helper script doesn't exist in solo challenge, pull from guided
    if mode == "solo" and not script_path.exists():
        guided_script = CHALLENGES_ROOT / entry["folder"] / script_name
        if guided_script.exists():
            print(f"📦 Pulling missing helper script from guided version: {guided_script}")
            script_dest = validation_folder / script_name
            script_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(guided_script, script_dest)
        else:
            print(f"❌ ERROR: Helper script {guided_script} not found in guided version.", file=sys.stderr)
            return False

    log_file = validation_folder / "validation.log"

    if not script_path.exists():
        print(f"❌ ERROR: Helper script {script_path} not found after fallback attempt.", file=sys.stderr)
        return False

    print(f"🚀 Running helper script: {script_path.name}")
    env = os.environ.copy()
    env["CCRI_VALIDATE"] = "1"
    env["CCRI_MODE"] = mode

    try:
        with open(log_file, "w", encoding="utf-8") as log:
            process = subprocess.Popen(
                ["python3", str(script_path)],
                cwd=validation_folder,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            for line in process.stdout:
                print(f"    🐍 {line.strip()}")
                log.write(line)
            result_code = process.wait()

        if result_code == 0:
            print(f"✅ {challenge_id}: Validation passed.")
            return True
        else:
            print(f"❌ {challenge_id}: Helper script returned non-zero exit code.")
            print(f"   🔗 See {log_file} for details.")
            return False

    except subprocess.TimeoutExpired:
        print(f"⏳ TIMEOUT: Helper script took too long for {challenge_id}.")
        with open(log_file, "a", encoding="utf-8") as log:
            log.write("\n⏳ TIMEOUT: Helper script exceeded time limit.\n")
        timeouts.append(challenge_id)
        return False

def choose_mode():
    print("\n🎛️ Which validation mode?")
    print("[1] Guided (default)")
    print("[2] Solo")
    choice = input("Enter choice [1/2]: ").strip()
    return "solo" if choice == "2" else "guided"

def main():
    print("\n🚦 CCRI STEMDay Master Validator\n" + "="*40)

    mode = sys.argv[1].lower() if len(sys.argv) > 1 else choose_mode()
    if mode not in ("guided", "solo"):
        print("❌ Invalid mode. Usage: validate_all_flags.py [guided|solo]")
        sys.exit(1)

    print(f"🛠️ Mode: {mode.upper()}")
    clean_validation_folder()
    challenges = load_challenges_json(mode)
    unlocks = load_validation_unlocks(mode)
    fallback_scripts = load_guided_scripts() if mode == "solo" else {}

    challenges_root = CHALLENGES_ROOT_SOLO if mode == "solo" else CHALLENGES_ROOT

    success_count = 0
    fail_count = 0
    timeouts = []

    for challenge_id, entry in challenges.items():
        if validate_challenge(challenge_id, entry, timeouts, challenges_root, mode, fallback_scripts):
            success_count += 1
        else:
            fail_count += 1

    print("\n📊 Validation Summary:")
    print(f"✅ {success_count} passed")
    print(f"❌ {fail_count} failed")
    if timeouts:
        print(f"⏳ {len(timeouts)} timed out: {', '.join(timeouts)}")
        print("⚠️ Check validation_results/*/validation.log for details.")

    if fail_count == 0 and not timeouts:
        print("\n🎉 All challenges validated successfully!\n")
    else:
        print("\n🚨 Validation completed with errors or timeouts. Review the logs above.\n")

if __name__ == "__main__":
    main()
