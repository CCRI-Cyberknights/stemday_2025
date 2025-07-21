#!/usr/bin/env python3

from pathlib import Path
import random
import codecs
import sys
import time
import json
from flag_generators.flag_helpers import FlagUtils


class ROT13FlagGenerator:
    """
    Generator for the ROT13 cipher challenge.
    Encodes an entire intercepted message (including flags) into cipher.txt.
    Stores unlock metadata for validation workflow.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo
        self.metadata = {}  # For unlock info

        # Choose correct unlocks file based on mode
        unlocks_filename = (
            "validation_unlocks_solo.json"
            if self.mode == "solo" else
            "validation_unlocks.json"
        )
        self.unlock_file = self.project_root / "web_version_admin" / unlocks_filename

    @staticmethod
    def find_project_root() -> Path:
        """Walk up directories until .ccri_ctf_root is found."""
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
        sys.exit(1)

    @staticmethod
    def rot13(text: str) -> str:
        """Apply ROT13 cipher to the given text."""
        return codecs.encode(text, "rot_13")

    def safe_cleanup(self, challenge_folder: Path):
        """Remove only generated assets from the challenge folder."""
        cipher_file = challenge_folder / "cipher.txt"
        if cipher_file.exists():
            try:
                cipher_file.unlink()
                print(f"🗑️ Removed old file: {cipher_file.name}")
            except Exception as e:
                print(f"⚠️ Could not delete {cipher_file.name}: {e}", file=sys.stderr)

    def update_validation_unlocks(self, real_flag: str, cipher_file: Path):
        """Save metadata into the correct validation_unlocks JSON."""
        try:
            # Load existing data
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            # Update metadata for this challenge
            unlocks["03_ROT13"] = {
                "real_flag": real_flag,
                "challenge_file": str(cipher_file.relative_to(self.project_root)),
                "unlock_method": "ROT13 decode",
                "hint": "Apply ROT13 to cipher.txt to recover plaintext."
            }

            # Save back to file
            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved to: {self.unlock_file.relative_to(self.project_root)}")

        except Exception as e:
            print(f"❌ Failed to update {self.unlock_file.name}: {e}", file=sys.stderr)
            sys.exit(1)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """Create cipher.txt in the challenge folder with ROT13-encoded message."""
        cipher_file = challenge_folder / "cipher.txt"

        # Clean up previous file
        self.safe_cleanup(challenge_folder)

        try:
            if not challenge_folder.exists():
                raise FileNotFoundError(
                    f"❌ Challenge folder not found: {challenge_folder.relative_to(self.project_root)}"
                )

            # Combine and shuffle flags
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            # Build plaintext message
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

            # ROT13 the message
            encoded_message = self.rot13(message)

            # Write to cipher.txt
            cipher_file.write_text(encoded_message)
            print(f"📄 {cipher_file.relative_to(self.project_root)} created with ROT13-encoded transmission.")

            # Update validation unlocks
            self.update_validation_unlocks(real_flag, cipher_file)

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {cipher_file.relative_to(self.project_root)}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate flags and embed them into cipher.txt.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        # Avoid accidental duplication of real flag
        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print("   🎭 Fake flags:", ", ".join(fake_flags))
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
