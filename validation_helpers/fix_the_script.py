#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data

CHALLENGE_ID = "09_FixScript"

def replace_operator(script_path: Path, new_operator: str):
    try:
        lines = script_path.read_text(encoding="utf-8").splitlines()
        fixed_lines = []
        for line in lines:
            if "code =" in line and any(op in line for op in ["+", "-", "*", "/"]):
                fixed_lines.append(f"code = part1 {new_operator} part2  # <- fixed math")
            else:
                fixed_lines.append(line)
        script_path.write_text("\n".join(fixed_lines) + "\n", encoding="utf-8")
    except Exception as e:
        print(f"❌ ERROR updating script: {e}", file=sys.stderr)
        sys.exit(1)

def run_python_script(script_path: Path) -> str:
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ ERROR: Python interpreter not found.", file=sys.stderr)
        sys.exit(1)

def main():
    root = find_project_root()
    data = load_unlock_data(root, CHALLENGE_ID)
    flag = data.get("real_flag")
    correct_op = data.get("correct_operator", "+")
    mode = os.environ.get("CCRI_MODE", "guided")

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    script_path = root / base_path / CHALLENGE_ID / "broken_flag.py"

    if not script_path.is_file():
        print(f"❌ ERROR: broken_flag.py not found at {script_path}", file=sys.stderr)
        sys.exit(1)

    replace_operator(script_path, correct_op)
    output = run_python_script(script_path)

    if flag in output:
        print(f"✅ Validation success: found flag {flag}")
        sys.exit(0)
    else:
        print(f"❌ Validation failed: flag {flag} not found in output.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
