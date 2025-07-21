#!/usr/bin/env python3

from pathlib import Path
import base64
import random
import json
import sys
from flag_generators.flag_helpers import FlagUtils


class Base64FlagGenerator:
    """
    Generator for the Base64 intercepted message challenge.
    Encodes an intercepted transmission (including flags) into encoded.txt
    and stores unlock metadata for validation workflow.
    """
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()
        self.metadata = {}  # For unlock info
        self.unlock_file = self.project_root / "web_version_admin" / "validation_unlocks.json"

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
        Remove only generated assets from the challenge folder.
        """
        encoded_file = challenge_folder / "encoded.txt"
        if encoded_file.exists():
            try:
                encoded_file.unlink()
                print(f"🗑️ Removed old file: {encoded_file.name}")
            except Exception as e:
                print(f"⚠️ Could not delete {encoded_file.name}: {e}", file=sys.stderr)

    def update_validation_unlocks(self):
        """
        Save self.metadata into validation_unlocks.json for 02_Base64.
        """
        try:
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            unlocks["02_Base64"] = self.metadata

            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved: {self.unlock_file.relative_to(self.project_root)}")
        except Exception as e:
            print(f"❌ Failed to update validation_unlocks.json: {e}", file=sys.stderr)
            sys.exit(1)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Create encoded.txt in the challenge folder with base64-encoded intercepted message.
        """
        encoded_file = challenge_folder / "encoded.txt"

        # Clean up only our generated file
        self.safe_cleanup(challenge_folder)

        try:
            if not challenge_folder.exists():
                raise FileNotFoundError(
                    f"❌ Challenge folder not found: {challenge_folder.relative_to(self.project_root)}"
                )

            # Combine and shuffle flags
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            # Build plaintext intercepted message
            message = (
                "Transmission Start\n"
                "------------------------\n"
                "To: LIBER8 Command Node\n"
                "From: Field Agent 4\n\n"
                "Flag candidates identified during network sweep. "
                "Message encoded for secure transit.\n\n"
                "Candidates:\n"
                + "\n".join(f"- {flag}" for flag in all_flags)
                + "\n\nVerify and submit the authentic CCRI flag.\n\n"
                "Transmission End\n"
                "------------------------\n"
            )

            # Base64 encode the entire message
            encoded_message = base64.b64encode(message.encode("utf-8")).decode("utf-8")

            # Write to encoded.txt
            encoded_file.write_text(encoded_message + "\n")
            print(f"📄 {encoded_file.relative_to(self.project_root)} created with Base64-encoded transmission.")

            # ✅ Record unlock metadata
            self.metadata = {
                "real_flag": real_flag,
                "challenge_file": str(encoded_file.relative_to(self.project_root)),
                "unlock_method": "Base64 decode",
                "hint": "Decode encoded.txt using base64 -d or an online tool."
            }

            # Save metadata to validation_unlocks.json
            self.update_validation_unlocks()

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {encoded_file.relative_to(self.project_root)}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate flags and embed them into encoded.txt.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        # Ensure real flag isn’t duplicated accidentally
        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ Admin flag: {real_flag}")
        return real_flag
