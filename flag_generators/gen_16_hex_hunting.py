#!/usr/bin/env python3
import os
import random
import sys
from pathlib import Path
from flag_generators.flag_helpers import FlagUtils


class HexHuntingFlagGenerator:
    """
    Generator for the Hex Hunting challenge.
    Embeds real and fake flags in a random binary file.
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

    @staticmethod
    def insert_flag(binary_data: bytearray, flag: str, offset: int):
        """
        Insert a flag string at a specific offset, with printable padding for discovery.
        """
        flag_bytes = flag.encode("utf-8")
        padded_flag = flag_bytes + b" " * random.randint(1, 3)  # Add space padding
        if offset + len(padded_flag) > len(binary_data):
            raise ValueError(f"❌ Offset {offset} + flag length {len(padded_flag)} exceeds binary size {len(binary_data)}")
        binary_data[offset:offset + len(padded_flag)] = padded_flag

    def generate_hex_file(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Generate hex_flag.bin in the challenge folder.
        """
        challenge_folder.mkdir(parents=True, exist_ok=True)
        output_path = challenge_folder / "hex_flag.bin"

        # Overwrite only hex_flag.bin
        if output_path.exists():
            try:
                output_path.unlink()
                print(f"🗑️ Removed old file: {output_path.name}")
            except Exception as e:
                print(f"⚠️ Could not remove {output_path.name}: {e}", file=sys.stderr)

        binary_size = random.randint(1024, 1536)
        binary_data = bytearray(os.urandom(binary_size))

        # Ensure binary is large enough for flag embedding
        longest_flag_len = max(len(real_flag), max(len(f) for f in fake_flags))
        if binary_size < longest_flag_len + 200:
            raise RuntimeError("❌ Binary size too small for safe flag embedding.")

        # Pick random non-overlapping offsets
        max_offset = binary_size - longest_flag_len - 1
        offsets = random.sample(range(100, max_offset), 5)

        # Insert real flag
        self.insert_flag(binary_data, real_flag, offsets[0])

        # Insert fake flags
        for flag, offset in zip(fake_flags, offsets[1:]):
            self.insert_flag(binary_data, flag, offset)

        # Write binary file
        output_path.write_bytes(binary_data)

        print(f"✅ hex_flag.bin generated in {challenge_folder.relative_to(self.project_root)}")
        print(f"   🏁 Real flag: {real_flag}")
        print(f"   🎭 Fake flags: {', '.join(fake_flags)}")

        # Record unlock metadata
        self.metadata = {
            "real_flag": real_flag,
            "challenge_file": str(output_path.relative_to(self.project_root)),
            "unlock_method": "Inspect hex_flag.bin with a hex editor or strings command to locate the flag",
            "hint": "Try running 'strings hex_flag.bin' or open it in a hex editor like bless or GHex."
        }

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate real and fake flags, embed them, and return the real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = list({FlagUtils.generate_fake_flag() for _ in range(4)})

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.generate_hex_file(challenge_folder, real_flag, fake_flags)
        return real_flag
