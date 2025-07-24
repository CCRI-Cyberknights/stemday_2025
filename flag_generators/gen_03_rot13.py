#!/usr/bin/env python3

from pathlib import Path
import random
import codecs
import sys
from flag_generators.flag_helpers import FlagUtils


class ROT13FlagGenerator:
    """
    Generator for the ROT13 cipher challenge.
    Encodes flags into cipher.txt using ROT13.
    Exports validation metadata via self.metadata for master script use.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo
        self.metadata = {}

    @staticmethod
    def find_project_root() -> Path:
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
        sys.exit(1)

    @staticmethod
    def rot13(text: str) -> str:
        return codecs.encode(text, "rot_13")

    def safe_cleanup(self, challenge_folder: Path):
        cipher_file = challenge_folder / "cipher.txt"
        if cipher_file.exists():
            try:
                cipher_file.unlink()
                print(f"🗑️ Removed old file: {cipher_file.name}")
            except Exception as e:
                print(f"⚠️ Could not delete {cipher_file.name}: {e}", file=sys.stderr)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        cipher_file = challenge_folder / "cipher.txt"
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
                "From: Recon Unit 5\n\n"
                "Flag candidates from intercepted communications. "
                "Message scrambled with a simple cipher for transit security.\n\n"
                "Candidates:\n"
                + "\n".join(f"- {flag}" for flag in all_flags)
                + "\n\nValidate and extract the correct CCRI flag.\n\n"
                "Transmission End\n"
                "------------------------\n"
            )

            encoded_message = self.rot13(message)
            cipher_file.write_text(encoded_message)
            print(f"📄 {cipher_file.relative_to(self.project_root)} created with ROT13-encoded transmission.")

            self.metadata = {
                "real_flag": real_flag,
                "challenge_file": str(cipher_file.relative_to(self.project_root)),
                "unlock_method": "ROT13 decode",
                "hint": "Apply ROT13 to cipher.txt to recover plaintext."
            }

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {cipher_file.relative_to(self.project_root)}")
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
        print("   🎭 Fake flags:", ", ".join(fake_flags))
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
