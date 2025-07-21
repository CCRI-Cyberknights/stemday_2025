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
    Stores unlock metadata for validation workflow.
    """

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()
        self.metadata = {}  # For unlock info

    @staticmethod
    def find_project_root() -> Path:
        """
        Walk up directories until .ccri_ctf_root is found.
        """
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
        sys.exit(1)

    def safe_cleanup(self, challenge_folder: Path):
        """
        Remove only previously generated files for this challenge.
        """
        targets = [
            challenge_folder / "hidden_flag",     # compiled binary
            challenge_folder / "hidden_flag.c"    # C source file
        ]
        for target in targets:
            if target.exists():
                try:
                    target.unlink()
                    print(f"🗑️ Removed old file: {target.relative_to(self.project_root)}")
                except Exception as e:
                    print(f"⚠️ Could not delete {target.name}: {e}", file=sys.stderr)

    def generate_c_source(self, real_flag: str, fake_flags: list) -> str:
        """
        Generate C source code with embedded real + fake flags.
        """
        junk_strings = [
            "ABCD1234XYZ!@#%$^&*()_+=?><~",
            "longgarbage....data...not...readable....random",
            "G@rb@g3StuffDataThatLooksBinaryButIsn't....",
            "%%%%%%%//////??????^^^^^*****&&&&&"
        ]
        binary_junk = ", ".join(str(random.randint(0, 255)) for _ in range(600))

        return f"""
#include <stdio.h>
#include <string.h>

// Embedded flags
char flag1[] = "{fake_flags[0]}";
char junk1[300] = "{junk_strings[0]}";

char flag2[] = "{real_flag}";
char junk2[500] = "{junk_strings[1]}";

char flag3[] = "{fake_flags[1]}";
char junk3[400] = "{junk_strings[2]}";

char flag4[] = "{fake_flags[2]}";
char junk4[600] = {{{binary_junk}}};

char flag5[] = "{fake_flags[3]}";
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
        """
        Generate C source, compile it, and place binary in challenge folder.
        """
        self.safe_cleanup(challenge_folder)

        try:
            # Paths
            c_file = challenge_folder / "hidden_flag.c"
            binary_file = challenge_folder / "hidden_flag"

            # Generate and write C source
            c_source = self.generate_c_source(real_flag, fake_flags)
            c_file.write_text(c_source)
            print(f"📄 C source created: {c_file.relative_to(self.project_root)}")

            # Compile C source
            result = subprocess.run(
                ["gcc", str(c_file), "-o", str(binary_file)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"❌ GCC failed:\n{result.stderr.strip()}")

            print(f"🔨 Compiled binary: {binary_file.relative_to(self.project_root)}")

            # Cleanup source file
            try:
                c_file.unlink()
                print(f"🧹 Cleaned up source file: {c_file.relative_to(self.project_root)}")
            except Exception as cleanup_err:
                print(f"⚠️ Warning: Could not remove {c_file.relative_to(self.project_root)}: {cleanup_err}")

            # Record unlock metadata
            self.metadata = {
                "real_flag": real_flag,
                "challenge_file": str(binary_file.relative_to(self.project_root)),
                "unlock_method": "Analyze binary with strings or a disassembler to find flags",
                "hint": "Try using 'strings hidden_flag' or load it in radare2."
            }

        except Exception as e:
            print(f"💥 ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate real/fake flags and embed them into binary.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ Admin flag: {real_flag}")
        return real_flag
