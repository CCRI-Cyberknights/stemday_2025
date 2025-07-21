#!/usr/bin/env python3

from pathlib import Path
import random
import sys
import json
from flag_generators.flag_helpers import FlagUtils


class FixScriptFlagGenerator:
    """
    Generator for the Fix the Script challenge.
    Embeds the real flag into a Python script with a broken operator.
    Handles guided and solo modes separately but uses the full operator set for both.
    """

    ALL_OPERATORS = ["+", "-", "*", "/"]

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo

        # Unlock metadata file based on mode
        unlock_file_name = (
            "validation_unlocks_solo.json"
            if self.mode == "solo" else
            "validation_unlocks.json"
        )
        self.unlock_file = self.project_root / "web_version_admin" / unlock_file_name
        self.metadata = {}

    @staticmethod
    def find_project_root() -> Path:
        """Walk up directories until .ccri_ctf_root is found."""
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
        sys.exit(1)

    def safe_cleanup(self, challenge_folder: Path):
        """Remove only the previously generated broken_flag.py file."""
        script_file = challenge_folder / "broken_flag.py"
        if script_file.exists():
            try:
                script_file.unlink()
                print(f"🗑️ Removed old file: {script_file.relative_to(self.project_root)}")
            except Exception as e:
                print(f"⚠️ Could not delete {script_file.name}: {e}", file=sys.stderr)

    def find_safe_parts_and_operator(self):
        """
        Keep trying until only 1 operator gives a 4-digit result.
        Uses ALL_OPERATORS for both guided and solo modes.
        """
        attempt = 0
        while True:
            attempt += 1
            correct_op = random.choice(self.ALL_OPERATORS)
            target_value = random.randint(1000, 9999)

            try:
                if correct_op == "+":
                    part1 = random.randint(100, target_value - 100)
                    part2 = target_value - part1
                elif correct_op == "-":
                    part1 = random.randint(target_value + 100, target_value + 1000)
                    part2 = part1 - target_value
                elif correct_op == "*":
                    factors = [i for i in range(2, 50) if target_value % i == 0]
                    if not factors:
                        continue
                    part2 = random.choice(factors)
                    part1 = target_value // part2
                elif correct_op == "/":
                    part2 = random.randint(2, 25)
                    part1 = target_value * part2
                else:
                    continue

                four_digit_ops = []
                for op in self.ALL_OPERATORS:
                    try:
                        result = eval(f"{part1} {op} {part2}")
                        if isinstance(result, int) and 1000 <= result <= 9999:
                            four_digit_ops.append(op)
                    except ZeroDivisionError:
                        continue

                if attempt % 100 == 0:
                    print(f"⏳ {attempt} attempts... Found {len(four_digit_ops)} ops with 4-digit results.")

                if four_digit_ops == [correct_op]:
                    print(f"✅ Found valid combination after {attempt} attempts!")
                    return correct_op, part1, part2, target_value

            except Exception as e:
                if attempt % 100 == 0:
                    print(f"⚠️ Attempt {attempt} error: {e}", file=sys.stderr)
                continue

    def update_validation_unlocks(self, real_flag: str, script_file: Path, correct_op: str):
        """Save metadata into the appropriate validation_unlocks JSON."""
        try:
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            unlocks["09_FixScript"] = {
                "real_flag": real_flag,
                "correct_operator": correct_op,
                "challenge_file": str(script_file.relative_to(self.project_root)),
                "unlock_method": "Fix the Python script’s math operator to calculate the flag",
                "hint": f"Find the broken operator in broken_flag.py and replace it with '{correct_op}'."
            }

            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved to: {self.unlock_file.relative_to(self.project_root)}")

        except Exception as e:
            print(f"❌ Failed to update {self.unlock_file.name}: {e}", file=sys.stderr)
            sys.exit(1)

    def embed_flag(self, challenge_folder: Path, suffix_value: int, correct_op: str, part1: int, part2: int):
        """Create broken_flag.py with randomized incorrect operator."""
        script_file = challenge_folder / "broken_flag.py"

        try:
            self.safe_cleanup(challenge_folder)

            challenge_folder.mkdir(parents=True, exist_ok=True)

            wrong_ops = [op for op in self.ALL_OPERATORS if op != correct_op]
            wrong_op = random.choice(wrong_ops)

            broken_script = f"""#!/usr/bin/env python3

# This script should print: CCRI-SCRP-{suffix_value}
# But someone broke the math!

part1 = {part1}
part2 = {part2}

# MATH ERROR!
code = part1 {wrong_op} part2  # <- wrong math

print(f"Your flag is: CCRI-SCRP-{{int(code)}}")
"""

            script_file.write_text(broken_script)
            script_file.chmod(0o755)

            print(f"📝 broken_flag.py created: {script_file.relative_to(self.project_root)}")
            print(f"✅ Correct op = {correct_op}, Broken op = {wrong_op}, Flag = CCRI-SCRP-{suffix_value}")

            # Save metadata
            real_flag = f"CCRI-SCRP-{suffix_value}"
            self.update_validation_unlocks(real_flag, script_file, correct_op)

        except Exception as e:
            print(f"💥 Failed to write script: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """Generate a real flag and embed it into broken_flag.py."""
        correct_op, part1, part2, suffix_value = self.find_safe_parts_and_operator()
        self.embed_flag(challenge_folder, suffix_value, correct_op, part1, part2)
        real_flag = f"CCRI-SCRP-{suffix_value}"
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
