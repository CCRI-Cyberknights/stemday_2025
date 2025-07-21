#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import base64
import json
import sys
from flag_generators.flag_helpers import FlagUtils


class ArchivePasswordFlagGenerator:
    """
    Generator for the Archive Password challenge.
    Embeds real and fake flags into a password-protected ZIP archive.
    Stores unlock metadata for validation workflow.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo
        self.wordlist_template = self.project_root / "flag_generators" / "wordlist.txt"

        # Select validation file based on mode
        unlocks_file = (
            "validation_unlocks_solo.json" if self.mode == "solo" else "validation_unlocks.json"
        )
        self.unlock_file = self.project_root / "web_version_admin" / unlocks_file
        self.metadata = {}

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
        Remove previously generated assets from the challenge folder.
        """
        for filename in ["wordlist.txt", "message_encoded.txt", "secret.zip"]:
            target_file = challenge_folder / filename
            if target_file.exists():
                try:
                    target_file.unlink()
                    print(f"🗑️ Removed old file: {target_file.name}")
                except Exception as e:
                    print(f"⚠️ Could not delete {target_file.name}: {e}", file=sys.stderr)

    def choose_password(self, all_passwords):
        """
        Select a password for the ZIP file depending on mode.
        """
        if self.mode == "guided":
            # Pick a random password from the lower half of the wordlist
            return random.choice(all_passwords[:len(all_passwords)//2])
        else:
            # Pick a random password from the upper half of the wordlist
            return random.choice(all_passwords[len(all_passwords)//2:])

    def update_validation_unlocks(self, real_flag: str, zip_file: Path, wordlist_file: Path, password: str):
        """
        Save metadata into the correct validation unlocks JSON file.
        """
        try:
            # Load existing unlocks file
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            # Add metadata for this challenge
            unlocks["05_ArchivePassword"] = {
                "real_flag": real_flag,
                "zip_password": password,
                "challenge_file": str(zip_file.relative_to(self.project_root)),
                "wordlist_file": str(wordlist_file.relative_to(self.project_root)),
                "unlock_method": "Brute-force ZIP password using provided wordlist",
                "hint": "Use wordlist.txt with zip2john + hashcat or fcrackzip."
            }

            # Save back to file
            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved: {self.unlock_file.relative_to(self.project_root)}")

        except Exception as e:
            print(f"❌ Failed to update {self.unlock_file.name}: {e}", file=sys.stderr)
            sys.exit(1)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Create wordlist.txt and password-protected secret.zip containing message_encoded.txt.
        """
        self.safe_cleanup(challenge_folder)

        try:
            if not challenge_folder.exists():
                raise FileNotFoundError(
                    f"❌ Challenge folder not found: {challenge_folder.relative_to(self.project_root)}"
                )

            if not self.wordlist_template.exists():
                raise FileNotFoundError(
                    f"❌ Wordlist template missing: {self.wordlist_template.relative_to(self.project_root)}"
                )

            # Load master wordlist
            all_passwords = self.wordlist_template.read_text().splitlines()
            if not all_passwords:
                raise ValueError("❌ Wordlist template is empty!")

            # Select password based on mode
            correct_password = self.choose_password(all_passwords)

            # Copy wordlist.txt into challenge folder
            wordlist_file = challenge_folder / "wordlist.txt"
            wordlist_file.write_text("\n".join(all_passwords))

            # Create message_encoded.txt (base64-encoded flags)
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)
            message = (
                "Mission Debrief:\n\n"
                "Encrypted transmission recovered from target machine.\n"
                "Analysis reveals five potential keys, but only one fits agency format.\n\n"
                "Decoded entries:\n" +
                "\n".join(f"- {flag}" for flag in all_flags) +
                "\n\nProceed with caution."
            )
            message_encoded = base64.b64encode(message.encode("utf-8")).decode("utf-8")

            encoded_file = challenge_folder / "message_encoded.txt"
            encoded_file.write_text(message_encoded)

            # Create password-protected ZIP (flat)
            zip_file = challenge_folder / "secret.zip"
            result = subprocess.run(
                ["zip", "-j", "-P", correct_password, str(zip_file), str(encoded_file.name)],
                cwd=challenge_folder,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"❌ Zip failed: {result.stderr.strip()}")

            # Clean up plaintext file
            encoded_file.unlink()
            print(f"🗝️ {wordlist_file.relative_to(self.project_root)} and 🔒 {zip_file.relative_to(self.project_root)} created with correct password: {correct_password}")

            # Save unlock metadata
            self.update_validation_unlocks(real_flag, zip_file, wordlist_file, correct_password)

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate and embed real/fake flags for the Archive Password challenge.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
