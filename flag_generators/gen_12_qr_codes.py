#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import sys
import json
from flag_generators.flag_helpers import FlagUtils


class QRCodeFlagGenerator:
    """
    Generator for the QR Codes challenge.
    Produces 5 QR code PNGs in the challenge folder with 1 real flag and 4 decoys.
    Supports guided and solo modes with separate unlock metadata.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo

        # Choose unlocks file based on mode
        unlock_file_name = (
            "validation_unlocks_solo.json"
            if self.mode == "solo" else
            "validation_unlocks.json"
        )
        self.unlock_file = self.project_root / "web_version_admin" / unlock_file_name
        self.metadata = {}

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
    def check_qrencode_installed():
        """Verify qrencode is installed, or exit with error."""
        result = subprocess.run(["which", "qrencode"], capture_output=True)
        if result.returncode != 0:
            print("❌ ERROR: qrencode is not installed.")
            print("👉 To fix, run: sudo apt install qrencode")
            sys.exit(1)
        else:
            print("✅ qrencode is installed.")

    def create_qr_code(self, output_file: Path, text: str):
        """Use qrencode to generate a QR code PNG."""
        try:
            subprocess.run(["qrencode", "-o", str(output_file), text], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate QR code: {e}", file=sys.stderr)
            sys.exit(1)

    def clean_qr_codes(self, folder: Path):
        """Remove only old QR codes (qr_*.png) in the challenge folder."""
        if folder.exists():
            try:
                for qr_file in folder.glob("qr_*.png"):
                    qr_file.unlink()
                    print(f"🗑️ Removed old QR code: {qr_file.name}")
            except Exception as e:
                print(f"⚠️ Could not delete QR code(s) in {folder.relative_to(self.project_root)}: {e}", file=sys.stderr)
        else:
            print(f"📁 Creating challenge folder: {folder.relative_to(self.project_root)}")
            folder.mkdir(parents=True, exist_ok=True)

    def update_validation_unlocks(self, real_flag: str, challenge_folder: Path):
        """Save metadata into the correct validation_unlocks JSON."""
        try:
            # Load existing unlocks
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            # Update for QRCode challenge
            unlocks["12_QRCodes"] = {
                "real_flag": real_flag,
                "challenge_folder": str(challenge_folder.relative_to(self.project_root)),
                "unlock_method": "Scan QR codes to reveal flags and find the real one",
                "hint": "Use a QR scanner app or zbarimg to read qr_*.png"
            }

            # Save back
            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved to: {self.unlock_file.relative_to(self.project_root)}")

        except Exception as e:
            print(f"❌ Failed to update {self.unlock_file.name}: {e}", file=sys.stderr)
            sys.exit(1)

    def embed_flags_as_qr(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Generate 5 QR codes in the challenge folder: 1 real flag and 4 fake flags.
        """
        self.clean_qr_codes(challenge_folder)

        # Combine and shuffle flags
        all_flags = fake_flags + [real_flag]
        random.shuffle(all_flags)

        print(f"🎭 Fake flags: {', '.join(fake_flags)}")
        print(f"🎯 Generating QR codes in: {challenge_folder.relative_to(self.project_root)}")

        for i, flag in enumerate(all_flags, start=1):
            qr_file = challenge_folder / f"qr_{i:02}.png"
            self.create_qr_code(qr_file, flag)
            if flag == real_flag:
                print(f"✅ {qr_file.name} (REAL flag)")
            else:
                print(f"➖ {qr_file.name} (decoy)")

        # Save unlock metadata
        self.update_validation_unlocks(real_flag, challenge_folder)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate QR code PNGs with 1 real and 4 fake flags.
        Return the real flag.
        """
        self.check_qrencode_installed()

        real_flag = FlagUtils.generate_real_flag()
        fake_flags = list({FlagUtils.generate_fake_flag() for _ in range(4)})

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags_as_qr(challenge_folder, real_flag, fake_flags)
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
