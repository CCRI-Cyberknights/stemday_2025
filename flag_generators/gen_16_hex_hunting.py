#!/usr/bin/env python3
import os
import random
import sys
from pathlib import Path
from typing import List, Tuple
from flag_generators.flag_helpers import FlagUtils


class HexHuntingFlagGenerator:
    """
    Generator for the Hex Hunting challenge.
    Embeds real and fake flags in a random binary file.
    Collects unlock metadata in self.metadata (no file writes).
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode
        self.metadata = {}

    @staticmethod
    def find_project_root() -> Path:
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker.", file=sys.stderr)
        sys.exit(1)

    @staticmethod
    def _choose_non_overlapping_offsets(
        bin_size: int,
        spans: List[int],
        start_min: int = 100
    ) -> List[int]:
        """
        Given the binary size and a list of span lengths (bytes) to place,
        return start offsets such that no spans overlap.
        """
        max_start = bin_size - max(spans) - 1
        if max_start <= start_min:
            raise RuntimeError("❌ Binary size too small for safe flag embedding.")

        chosen: List[Tuple[int, int]] = []  # (start, end) inclusive
        offsets: List[int] = []

        for span in spans:
            # Try many times to find a non-overlapping start
            for _ in range(10_000):
                s = random.randint(start_min, max_start)
                e = s + span - 1
                # overlap if not (new end < old start or new start > old end)
                if any(not (e < a or s > b) for a, b in chosen):
                    continue
                chosen.append((s, e))
                offsets.append(s)
                break
            else:
                raise RuntimeError("❌ Could not find non-overlapping offsets; increase binary size or reduce spans.")
        return offsets

    @staticmethod
    def insert_flag(binary_data: bytearray, flag: str, offset: int, pad_len: int):
        """Insert a flag string at a specific offset with exact padded spacing."""
        flag_bytes = flag.encode("utf-8")
        padded_flag = flag_bytes + (b" " * pad_len)
        if offset + len(padded_flag) > len(binary_data):
            raise ValueError(
                f"❌ Offset {offset} + flag length {len(padded_flag)} exceeds binary size {len(binary_data)}"
            )
        binary_data[offset:offset + len(padded_flag)] = padded_flag

    def generate_hex_file(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """Create hex_flag.bin and embed the flags with guaranteed non-overlap."""
        challenge_folder.mkdir(parents=True, exist_ok=True)
        output_path = challenge_folder / "hex_flag.bin"

        if output_path.exists():
            try:
                output_path.unlink()
                print(f"🗑️ Removed old file: {output_path.name}")
            except Exception as e:
                print(f"⚠️ Could not remove {output_path.name}: {e}", file=sys.stderr)

        # Size big enough to comfortably place 5 spans with padding
        binary_size = random.randint(1024, 1536)
        binary_data = bytearray(os.urandom(binary_size))

        # Pre-decide EXACT pads so we know the exact spans before choosing offsets
        pads = [random.randint(1, 3) for _ in range(1 + len(fake_flags))]
        spans = [len(real_flag) + pads[0]] + [len(f) + p for f, p in zip(fake_flags, pads[1:])]

        # Sanity check
        longest_flag_len = max(len(real_flag), *(len(f) for f in fake_flags))
        if binary_size < longest_flag_len + 200:
            raise RuntimeError("❌ Binary size too small for safe flag embedding.")

        # Choose non-overlapping offsets for [real] + [fakes]
        offsets = self._choose_non_overlapping_offsets(binary_size, spans, start_min=100)

        # Insert: real first, then fakes (order doesn’t matter thanks to non-overlap)
        self.insert_flag(binary_data, real_flag, offsets[0], pads[0])
        for flag, off, pad in zip(fake_flags, offsets[1:], pads[1:]):
            self.insert_flag(binary_data, flag, off, pad)

        output_path.write_bytes(binary_data)

        print(f"✅ hex_flag.bin generated in {challenge_folder.relative_to(self.project_root)}")
        print(f"   🏁 Real flag: {real_flag}")
        print(f"   🎭 Fake flags: {', '.join(fake_flags)}")

        self.metadata = {
            "real_flag": real_flag,
            "challenge_file": str(output_path.relative_to(self.project_root)),
            "unlock_method": "Inspect hex_flag.bin with a hex editor or strings command to locate the flag",
            "hint": "Try running 'strings hex_flag.bin' or open it in a hex editor like bless or GHex."
        }

    def generate_flag(self, challenge_folder: Path) -> str:
        real_flag = FlagUtils.generate_real_flag()

        # Ensure EXACTLY 4 unique fakes (set + loop to avoid <4 due to duplicates)
        fake_set = set()
        while len(fake_set) < 4:
            fake_set.add(FlagUtils.generate_fake_flag())
        fake_flags = list(fake_set)

        # Fakes never start with CCRI by design, so no collision with real prefix
        self.generate_hex_file(challenge_folder, real_flag, fake_flags)

        # Update metadata for master script
        self.metadata = {
            "real_flag": real_flag,
            "challenge_file": str((challenge_folder / "hex_flag.bin").relative_to(self.project_root)),
            "unlock_method": "Inspect hex_flag.bin with a hex editor or strings command to locate the flag",
            "hint": "Try running 'strings hex_flag.bin' or open it in a hex editor like bless or GHex."
        }

        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
