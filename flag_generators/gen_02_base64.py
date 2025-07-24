#!/usr/bin/env python3

from pathlib import Path
import base64
import random
import sys
from flag_generators.flag_helpers import FlagUtils


class Base64FlagGenerator:
    """
    Generator for the Base64 intercepted message challenge.
    Encodes an intercepted transmission (including flags) into encoded.txt.
    Supports Guided and Solo modes. Unlock metadata is exported via self.metadata.
    """

    def __init__(self, project_root: Path = None, mode: str = "guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode.lower()
        if self.mode not in ["guided", "solo"]:
            print(f"❌ ERROR: Invalid mode '{self.mode}'. Expected 'guided' or 'solo'.", file=sys.stderr)
            sys.exit(1)

        self.metadata = {}

    @staticmethod
    def find_project_root() -> Path:
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
        sys.exit(1)

    def safe_cleanup(self, challenge_folder: Path):
        encoded_file = challenge_folder / "encoded.txt"
        if encoded_file.exists():
            try:
                encoded_file.unlink()
                print(f"🗑️ Removed old file: {encoded_file.name}")
            except Exception as e:
                print(f"⚠️ Could not delete {encoded_file.name}: {e}", file=sys.stderr)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        encoded_file = challenge_folder / "encoded.txt"
        self.safe_cleanup(challenge_folder)

        try:
            if not challenge_folder.exists():
                raise FileNotFoundError(f"❌ Challenge folder not found: {challenge_folder.relative_to(self.project_root)}")

            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            message = (
                "Transmission Start\n"
                "------------------------\n"
                "To: LIBER8 Command Node\n"
                "From: Field Agent 4\n\n"
                "Flag candidates identified during network sweep. "
                "Message encoded for secure transit.\n\n"
                "Candidates:\n" +
                "\n".join(f"- {flag}" for flag in all_flags) +
                "\n\nVerify and submit the authentic CCRI flag.\n\n"
                "Transmission End\n"
                "------------------------\n"
            )

            encoded_message = base64.b64encode(message.encode("utf-8")).decode("utf-8")
            encoded_file.write_text(encoded_message + "\n")
            print(f"📄 {encoded_file.relative_to(self.project_root)} created with Base64-encoded transmission.")

            # Store metadata for validation
            self.metadata = {
                "real_flag": real_flag,
                "challenge_file": str(encoded_file.relative_to(self.project_root)),
                "unlock_method": "Base64 decode",
                "hint": "Decode encoded.txt using base64 -d or an online tool."
            }

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {encoded_file.relative_to(self.project_root)}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
