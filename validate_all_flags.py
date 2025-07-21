#!/usr/bin/env python3
import subprocess
import shutil
import sys
import os
from pathlib import Path
import json

# === CCRI STEMDay Master Validator ===
VALIDATION_ROOT = Path.cwd() / "validation_results"
CHALLENGES_ROOT = Path.cwd() / "challenges"
CHALLENGES_JSON = Path.cwd() / "web_version_admin" / "challenges.json"

# Timeout in seconds for each helper script
HELPER_TIMEOUT = 30

# Verbose logging flag
VERBOSE = True

def log_verbose(message):
    """Print detailed debug info if verbose mode is enabled."""
    if VERBOSE:
        print(f"📝 [VERBOSE] {message}")

def clean_validation_folder():
    """Remove old validation results and create a fresh folder."""
    if VALIDATION_ROOT.exists():
        print("🧹 Cleaning old validation_results...")
        log_verbose(f"Removing: {VALIDATION_ROOT}")
        shutil.rmtree(VALIDATION_ROOT)
    VALIDATION_ROOT.mkdir()
    print("📁 Created fresh validation_results/ folder.")
    log_verbose(f"Created: {VALIDATION_ROOT}")

def load_challenges_json():
    """Load challenges.json for real flags and script paths."""
    log_verbose(f"Loading challenge metadata from: {CHALLENGES_JSON}")
    if not CHALLENGES_JSON.exists():
        print(f"❌ ERROR: {CHALLENGES_JSON} not found.", file=sys.stderr)
        sys.exit(1)
    with open(CHALLENGES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        log_verbose(f"Loaded {len(data)} challenges.")
        return data

def copy_root_marker():
    """Copy .ccri_ctf_root marker into the sandbox root if it exists."""
    marker = Path(".ccri_ctf_root")
    dest = VALIDATION_ROOT.parent / ".ccri_ctf_root"

    if marker.exists():
        if dest.resolve() != marker.resolve():
            shutil.copy2(marker, dest)
            log_verbose(f"Copied .ccri_ctf_root marker into sandbox root: {dest}")
        else:
            log_verbose(f".ccri_ctf_root already in sandbox root, skipping copy: {dest}")
    else:
        log_verbose("No .ccri_ctf_root marker found at project root.")


def validate_challenge(challenge_id, entry, timeouts):
    """Validate a single challenge in an isolated sandbox."""
    print(f"\n🔍 Validating {challenge_id}: {entry['name']}...")
    original_folder = CHALLENGES_ROOT / entry["folder"]
    validation_folder = VALIDATION_ROOT / entry["folder"]
    validation_folder.mkdir(parents=True, exist_ok=True)
    log_verbose(f"Original folder: {original_folder}")
    log_verbose(f"Validation folder: {validation_folder}")

    # Copy all challenge contents (including helper script)
    for item in original_folder.iterdir():
        dest = validation_folder / item.name
        if item.is_dir():
            log_verbose(f"Copying folder: {item} -> {dest}")
            shutil.copytree(item, dest)
        else:
            log_verbose(f"Copying file: {item} -> {dest}")
            shutil.copy2(item, dest)

    # Paths
    script_path = validation_folder / entry["script"]  # Run helper script in sandbox
    log_file = validation_folder / "validation.log"
    log_verbose(f"Helper script path (sandboxed): {script_path}")
    log_verbose(f"Log file path: {log_file}")

    if not script_path.exists():
        print(f"❌ ERROR: Helper script {script_path} not found.", file=sys.stderr)
        return False

    print(f"🚀 Running helper script: {script_path.name}")
    env = os.environ.copy()
    env["CCRI_VALIDATE"] = "1"
    log_verbose(f"Environment variable CCRI_VALIDATE=1 set for subprocess.")
    log_verbose(f"Running subprocess: python3 {script_path} (cwd={validation_folder})")

    try:
        # Run subprocess and stream output live
        with open(log_file, "w", encoding="utf-8") as log:
            process = subprocess.Popen(
                ["python3", str(script_path)],
                cwd=validation_folder,  # Run from sandbox folder
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            # Stream stdout live to terminal and write to log
            for line in process.stdout:
                print(f"    🐍 {line.strip()}")
                log.write(line)

            result_code = process.wait()
            log_verbose(f"Subprocess completed with return code: {result_code}")

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
        log_verbose(f"Helper script for {challenge_id} exceeded {HELPER_TIMEOUT}s timeout.")
        timeouts.append(challenge_id)
        return False

def main():
    print("\n🚦 CCRI STEMDay Master Validator\n" + "="*40)
    clean_validation_folder()
    copy_root_marker()
    challenges = load_challenges_json()
    success_count = 0
    fail_count = 0
    timeouts = []

    for challenge_id, entry in challenges.items():
        log_verbose(f"Starting validation for {challenge_id}")
        if validate_challenge(challenge_id, entry, timeouts):
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
        print("\n🎉 All challenges validated successfully! The student workflow is working perfectly.\n")
    else:
        print("\n🚨 Validation completed with errors or timeouts. Review the logs above.\n")

if __name__ == "__main__":
    main()
