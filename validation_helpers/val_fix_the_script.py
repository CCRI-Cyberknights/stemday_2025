#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "09_FixScript"

def replace_operator(script_path: Path, new_operator: str) -> bool:
    try:
        lines = script_path.read_text(encoding="utf-8").splitlines()
        fixed_lines = []
        for line in lines:
            if "code =" in line and any(op in line for op in ["+", "-", "*", "/"]):
                fixed_lines.append(f"code = part1 {new_operator} part2  # <- fixed math")
            else:
                fixed_lines.append(line)
        script_path.write_text("\n".join(fixed_lines) + "\n", encoding="utf-8")
        return True
    except Exception as e:
        print(f"❌ ERROR updating script: {e}", file=sys.stderr)
        return False

def run_python_script(script_path: Path) -> str:
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ ERROR running script: {e}", file=sys.stderr)
        return ""

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    flag = data.get("real_flag")
    correct_op = data.get("correct_operator", "+")

    base_path = "challenges_solo" if mode == "solo" else "challenges"
    script_path = root / base_path / challenge_id / "broken_flag.py"

    if not script_path.is_file():
        print(f"❌ ERROR: broken_flag.py not found at {script_path}", file=sys.stderr)
        return False

    if not replace_operator(script_path, correct_op):
        return False

    output = run_python_script(script_path)
    if flag in output:
        print(f"✅ Validation success: found flag {flag}")
        return True
    else:
        print(f"❌ Validation failed: flag {flag} not found in output.", file=sys.stderr)
        return False

    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    from common import get_ctf_mode
    mode = get_ctf_mode()
    success = validate(mode=mode)
    import sys; sys.exit(0 if success else 1)
