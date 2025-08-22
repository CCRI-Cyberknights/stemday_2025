#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import sys
from flag_generators.flag_helpers import FlagUtils


class ExtractBinaryFlagGenerator:
    """
    Generator for the Extract Binary challenge.
    Embeds real and fake flags into a compiled C binary.
    Metadata is collected for the master script to handle unlocks.json.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo
        self.metadata = {}

    @staticmethod
    def find_project_root() -> Path:
        """Walk up directories until .ccri_ctf_root is found."""
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker.", file=sys.stderr)
        sys.exit(1)

    def safe_cleanup(self, challenge_folder: Path):
        """Remove generated binary and source."""
        for filename in ["hidden_flag", "hidden_flag.c"]:
            target = challenge_folder / filename
            if target.exists():
                try:
                    target.unlink()
                    print(f"🗑️ Removed old file: {target.relative_to(self.project_root)}")
                except Exception as e:
                    print(f"⚠️ Could not delete {target.name}: {e}", file=sys.stderr)

    def generate_c_source(self, real_flag: str, fake_flags: list) -> str:
        """Generate the C source code embedding all flags and junk data."""
        junk_strings = [
            "ABCD1234XYZ!@#%$^&*()_+=?><~",
            "longgarbage....data...not...readable....random",
            "G@rb@g3StuffDataThatLooksBinaryButIsn't....",
            "%%%%%%%//////??????^^^^^*****&&&&&"
        ]

        if self.mode == "solo":
            junk_strings = [s[::-1] + "_solo" for s in junk_strings]

        binary_junk = ", ".join(str(random.randint(0, 255)) for _ in range(600))

        # Note: __attribute__((used)) is optional but helps if you enable section GC/LTO.
        return f"""
#include <stdio.h>
#include <string.h>

__attribute__((used)) char flag1[] = "{fake_flags[0]}";
char junk1[300] = "{junk_strings[0]}";

__attribute__((used)) char flag2[] = "{real_flag}";
char junk2[500] = "{junk_strings[1]}";

__attribute__((used)) char flag3[] = "{fake_flags[1]}";
char junk3[400] = "{junk_strings[2]}";

__attribute__((used)) char flag4[] = "{fake_flags[2]}";
char junk4[600] = {{{binary_junk}}};

__attribute__((used)) char flag5[] = "{fake_flags[3]}";
char junk5[350] = "{junk_strings[3]}";

void keep_strings_alive() {{
    volatile char dummy = 0;
    dummy += flag1[0] + flag2[0] + flag3[0] + flag4[0] + flag5[0];
    dummy += junk1[0] + junk2[0] + junk3[0] + junk4[0] + junk5[0];
}}

int main() {{
    printf("Hello, world!\\n");
    keep_strings_alive();
    return 0;
}}
"""

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """Compile the challenge binary with embedded flags and collect metadata."""
        self.safe_cleanup(challenge_folder)

        try:
            c_file = challenge_folder / "hidden_flag.c"
            binary_file = challenge_folder / "hidden_flag"

            # Write source
            c_code = self.generate_c_source(real_flag, fake_flags)
            c_file.write_text(c_code)
            print(f"📄 C source created: {c_file.relative_to(self.project_root)}")

            # Compile
            result = subprocess.run(["gcc", str(c_file), "-o", str(binary_file)],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"❌ GCC failed:\n{result.stderr.strip()}")

            print(f"🔨 Compiled binary: {binary_file.relative_to(self.project_root)}")

            # Optional cleanup
            try:
                c_file.unlink()
                print(f"🧹 Cleaned up source file: {c_file.relative_to(self.project_root)}")
            except Exception as cleanup_err:
                print(f"⚠️ Warning: Could not remove {c_file.name}: {cleanup_err}")

            # Save metadata
            self.metadata = {
                "real_flag": real_flag,
                "challenge_file": str(binary_file.relative_to(self.project_root)),
                "unlock_method": "Analyze binary with strings or disassembler to find flags",
                "hint": "Try using 'strings hidden_flag' or load it in radare2."
            }

        except Exception as e:
            print(f"💥 ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """Generate and embed flag. Return real flag."""
        real_flag = FlagUtils.generate_real_flag()

        # Ensure EXACTLY 4 unique fakes
        fake_set = set()
        while len(fake_set) < 4:
            fake_set.add(FlagUtils.generate_fake_flag())
        fake_flags = list(fake_set)

        # real != fakes by construction (fakes never start with 'CCRI')
        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print("   🎭 Fake flags:", ", ".join(fake_flags))
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
