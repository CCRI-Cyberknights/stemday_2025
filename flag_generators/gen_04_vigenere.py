#!/usr/bin/env python3

from pathlib import Path
import random
import sys
from flag_generators.flag_helpers import FlagUtils


class VigenereFlagGenerator:
    """
    Generator for the Vigenère cipher challenge.
    Embeds encrypted flag message into cipher.txt.
    Exports validation metadata via self.metadata for use by the master script.
    """

    DEFAULT_KEY = "login"
    SOLO_KEY = "providence"

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo
        self.vigenere_key = (
            self.DEFAULT_KEY.lower() if self.mode == "guided" else self.SOLO_KEY.lower()
        )
        self.metadata = {}

    @staticmethod
    def find_project_root() -> Path:
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
        sys.exit(1)

    def vigenere_encrypt(self, plaintext: str, key: str = None) -> str:
        key = (key or self.vigenere_key).lower()
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
                result.append(char)
        return ''.join(result)

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
                raise FileNotFoundError(
                    f"❌ Challenge folder not found: {challenge_folder.relative_to(self.project_root)}"
                )

            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            # 🔥 Updated only the lore text inside the message
            message = (
                "Transmission Start\n"
                "------------------------\n"
                "To: CryptKeepers Command Node\n"
                "From: Field Unit 7\n\n"
                "Status update: Multiple potential flags recovered while monitoring "
                "CryptKeepers relay traffic. Data has been encoded prior to relay transfer.\n\n"
                "Candidates:\n"
                + "\n".join(f"- {flag}" for flag in all_flags)
                + "\n\nVerify the true CCRI flag before submission.\n\n"
                "Transmission End\n"
                "------------------------\n"
            )

            encrypted_message = self.vigenere_encrypt(message)
            cipher_file.write_text(encrypted_message)
            print(f"📄 {cipher_file.relative_to(self.project_root)} created with Vigenère-encrypted transmission.")

            self.metadata = {
                "real_flag": real_flag,
                "vigenere_key": self.vigenere_key,
                "challenge_file": str(cipher_file.relative_to(self.project_root)),
                "unlock_method": f"Vigenère cipher (key='{self.vigenere_key}')",
                "hint": f"Use the Vigenère key '{self.vigenere_key}' to decrypt cipher.txt."
            }

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {cipher_file.relative_to(self.project_root)}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error during embedding: {e}")
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
