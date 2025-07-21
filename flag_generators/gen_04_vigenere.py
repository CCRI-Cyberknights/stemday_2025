#!/usr/bin/env python3

from pathlib import Path
import random
import sys
from flag_generators.flag_helpers import FlagUtils


class VigenereFlagGenerator:
    """
    Generator for the Vigenère cipher challenge.
    Encodes an intercepted transmission (including flags) into cipher.txt.
    Stores unlock metadata for validation workflow.
    """
    VIGENERE_KEY = "login"  # Lowercase for consistency

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

    @classmethod
    def vigenere_encrypt(cls, plaintext: str, key: str = None) -> str:
        """
        Encrypt plaintext using Vigenère cipher with the given key.
        Mirrors decryption logic to ensure perfect round-trip.
        """
        key = (key or cls.VIGENERE_KEY).lower()  # Force lowercase
        result = []
        key_len = len(key)
        key_indices = [ord(k) - ord('a') for k in key]
        key_pos = 0

        for char in plaintext:
            if char.isalpha():
                offset = ord('A') if char.isupper() else ord('a')
                pi = ord(char) - offset
                ki = key_indices[key_pos % key_len]
                encrypted = chr((pi + ki) % 26 + offset)
                result.append(encrypted)
                key_pos += 1
            else:
                result.append(char)  # Leave non-alpha chars unchanged
        return ''.join(result)

    def safe_cleanup(self, challenge_folder: Path):
        """
        Remove only generated assets from the challenge folder.
        """
        cipher_file = challenge_folder / "cipher.txt"
        if cipher_file.exists():
            try:
                cipher_file.unlink()
                print(f"🗑️ Removed old file: {cipher_file.name}")
            except Exception as e:
                print(f"⚠️ Could not delete {cipher_file.name}: {e}", file=sys.stderr)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Create cipher.txt in the challenge folder with a Vigenère-encrypted message.
        """
        cipher_file = challenge_folder / "cipher.txt"

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

            # Build plaintext message
            message = (
                "Transmission Start\n"
                "------------------------\n"
                "To: LIBER8 Command Node\n"
                "From: Field Unit 7\n\n"
                "Status report: Flag candidates identified during operation. "
                "Data has been encoded for secure transit.\n\n"
                "Candidates:\n"
                + "\n".join(f"- {flag}" for flag in all_flags)
                + "\n\nVerify the true flag before submission.\n\n"
                "Transmission End\n"
                "------------------------\n"
            )

            # Encrypt the entire message
            encrypted_message = self.vigenere_encrypt(message)

            # Write to cipher.txt
            cipher_file.write_text(encrypted_message)
            print(f"📝 {cipher_file.relative_to(self.project_root)} created with Vigenère-encrypted transmission.")

            # Record unlock metadata
            self.metadata = {
                "real_flag": real_flag,
                "last_password": self.VIGENERE_KEY,
                "challenge_file": str(cipher_file.relative_to(self.project_root)),
                "vigenere_key": self.VIGENERE_KEY,
                "unlock_method": f"Vigenère cipher (key='{self.VIGENERE_KEY}')",
                "hint": "Use the Vigenère key to decrypt cipher.txt."
            }

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {cipher_file.relative_to(self.project_root)}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error during embedding: {e}")
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate a real flag and embed it into cipher.txt.
        Returns plaintext real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        # Ensure no accidental duplicate
        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ Admin flag: {real_flag}")
        return real_flag
