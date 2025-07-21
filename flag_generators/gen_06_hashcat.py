#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import hashlib
import base64
import sys
import json
from flag_generators.flag_helpers import FlagUtils


class HashcatFlagGenerator:
    """
    Generator for the Hashcat challenge.
    Splits flags into parts, encodes them, and creates password-protected zips.
    Handles separate passwords and unlock metadata for guided/solo modes.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo

        # Choose unlock file based on mode
        unlock_file_name = (
            "validation_unlocks_solo.json"
            if self.mode == "solo" else
            "validation_unlocks.json"
        )
        self.unlock_file = self.project_root / "web_version_admin" / unlock_file_name
        self.metadata = {}  # For unlock info

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
    def md5_hash(password: str) -> str:
        """Return MD5 hash of a password."""
        return hashlib.md5(password.encode("utf-8")).hexdigest()

    @staticmethod
    def base64_encode(text: str) -> str:
        """Base64 encode the given text."""
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    def safe_cleanup(self, challenge_folder: Path):
        """Remove previously generated assets (ZIPs, hashes.txt, wordlist.txt, encoded segments)."""
        targets = [
            challenge_folder / "hashes.txt",
            challenge_folder / "wordlist.txt",
            *challenge_folder.glob("encoded_segments*.txt"),
        ]
        segments_dir = challenge_folder / "segments"
        if segments_dir.exists():
            targets += list(segments_dir.glob("*.zip"))

        for target in targets:
            if target.exists():
                try:
                    target.unlink()
                    print(f"🗑️ Removed old file: {target.relative_to(self.project_root)}")
                except Exception as e:
                    print(f"⚠️ Could not delete {target.name}: {e}", file=sys.stderr)

    def update_validation_unlocks(self, real_flag):
        """Save metadata into the correct validation_unlocks JSON."""
        try:
            # Load existing data
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            # Update metadata for this challenge
            unlocks["06_Hashcat"] = self.metadata

            # Save back to file
            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved to: {self.unlock_file.relative_to(self.project_root)}")

        except Exception as e:
            print(f"❌ Failed to update {self.unlock_file.name}: {e}", file=sys.stderr)
            sys.exit(1)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """Create hashes.txt, wordlist.txt, and password-protected ZIPs with encoded segments."""
        self.safe_cleanup(challenge_folder)

        try:
            segments_dir = challenge_folder / "segments"
            segments_dir.mkdir(parents=True, exist_ok=True)

            # Combine and shuffle flags
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            # Split flags into parts
            parts = []
            for flag in all_flags:
                split_parts = flag.replace("-", " ").split()
                if len(split_parts) < 3:
                    split_parts += ["XXXX"] * (3 - len(split_parts))  # pad missing parts
                parts.append(split_parts[:3])

            part1 = [p[0] for p in parts]
            part2 = [p[1] for p in parts]
            part3 = [p[2] for p in parts]

            # Write base64-encoded segment files
            encoded_files = []
            for idx, segment in enumerate([part1, part2, part3], start=1):
                encoded_text = "\n".join(segment)
                encoded_b64 = self.base64_encode(encoded_text)
                file_path = challenge_folder / f"encoded_segments{idx}.txt"
                file_path.write_text(encoded_b64)
                encoded_files.append(file_path)

            # Pick random passwords (separate for guided/solo)
            wordlist_template = self.project_root / "flag_generators" / "wordlist.txt"
            all_passwords = wordlist_template.read_text().splitlines()
            chosen_passwords = random.sample(all_passwords, 3)

            # Create hashes.txt and mapping
            hashes_txt = challenge_folder / "hashes.txt"
            hashes_txt.write_text("")
            hash_password_zip_map = {}

            for idx, (password, file) in enumerate(zip(chosen_passwords, encoded_files), start=1):
                hash_val = self.md5_hash(password)
                hashes_txt.write_text(hashes_txt.read_text() + hash_val + "\n")

                zip_file = segments_dir / f"part{idx}.zip"
                result = subprocess.run(
                    ["zip", "-j", "-P", password, str(zip_file), str(file)],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    raise RuntimeError(f"❌ Zip failed for {file.name}: {result.stderr.strip()}")

                file.unlink()
                hash_password_zip_map[hash_val] = {
                    "password": password,
                    "zip_file": str(zip_file.relative_to(self.project_root))
                }

            # Copy shared wordlist.txt into challenge folder
            wordlist_file = challenge_folder / "wordlist.txt"
            wordlist_file.write_text("\n".join(all_passwords))

            print(
                f"🗝️ {hashes_txt.relative_to(self.project_root)}, "
                f"{wordlist_file.relative_to(self.project_root)}, "
                f"and 🔒 {segments_dir.relative_to(self.project_root)} created "
                f"with random passwords: {', '.join(chosen_passwords)}"
            )

            # Record unlock metadata with full mapping
            self.metadata = {
                "real_flag": real_flag,
                "reconstructed_flag": real_flag,
                "challenge_files": {
                    "hashes": str(hashes_txt.relative_to(self.project_root)),
                    "wordlist": str(wordlist_file.relative_to(self.project_root)),
                    "segments_dir": str(segments_dir.relative_to(self.project_root)),
                },
                "hash_password_zip_map": hash_password_zip_map,
                "unlock_method": "Recover MD5 hashes with Hashcat and unzip protected parts",
                "hint": "Use hashes.txt + wordlist.txt with Hashcat to crack passwords and extract ZIPs."
            }

            # Save metadata
            self.update_validation_unlocks(real_flag)

        except Exception as e:
            print(f"❌ Unexpected error during Hashcat setup: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """Generate real/fake flags and embed them into Hashcat challenge assets."""
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
