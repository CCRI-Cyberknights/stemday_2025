#!/usr/bin/env python3

import argparse
import sys
import shutil
import json
from pathlib import Path

# === Import backend classes ===
sys.path.insert(0, str(Path(__file__).resolve().parent / "web_version_admin"))
from ChallengeList import ChallengeList
from Challenge import Challenge

# === Import all generators ===
from flag_generators.gen_01_stego import StegoFlagGenerator
from flag_generators.gen_02_base64 import Base64FlagGenerator
from flag_generators.gen_03_rot13 import ROT13FlagGenerator
from flag_generators.gen_04_vigenere import VigenereFlagGenerator
from flag_generators.gen_05_archive_password import ArchivePasswordFlagGenerator
from flag_generators.gen_06_hashcat import HashcatFlagGenerator
from flag_generators.gen_07_extract_binary import ExtractBinaryFlagGenerator
from flag_generators.gen_08_fake_auth_log import FakeAuthLogFlagGenerator
from flag_generators.gen_09_fix_script import FixScriptFlagGenerator
from flag_generators.gen_10_metadata import MetadataFlagGenerator
from flag_generators.gen_11_hidden_flag import HiddenFlagGenerator
from flag_generators.gen_12_qr_codes import QRCodeFlagGenerator
from flag_generators.gen_13_http_headers import HTTPHeaderFlagGenerator
from flag_generators.gen_14_subdomain_sweep import SubdomainSweepFlagGenerator
from flag_generators.gen_15_process_inspection import ProcessInspectionFlagGenerator
from flag_generators.gen_16_hex_hunting import HexHuntingFlagGenerator
from flag_generators.gen_17_nmap_scanning import NmapScanFlagGenerator
from flag_generators.gen_18_pcap_search import PcapSearchFlagGenerator

# === Mapping challenge IDs to generator classes ===
GENERATOR_CLASSES = {
    "01_Stego": StegoFlagGenerator,
    "02_Base64": Base64FlagGenerator,
    "03_ROT13": ROT13FlagGenerator,
    "04_Vigenere": VigenereFlagGenerator,
    "05_ArchivePassword": ArchivePasswordFlagGenerator,
    "06_Hashcat": HashcatFlagGenerator,
    "07_ExtractBinary": ExtractBinaryFlagGenerator,
    "08_FakeAuthLog": FakeAuthLogFlagGenerator,
    "09_FixScript": FixScriptFlagGenerator,
    "10_Metadata": MetadataFlagGenerator,
    "11_HiddenFlag": HiddenFlagGenerator,
    "12_QRCodes": QRCodeFlagGenerator,
    "13_HTTPHeaders": HTTPHeaderFlagGenerator,
    "14_SubdomainSweep": SubdomainSweepFlagGenerator,
    "15_ProcessInspection": ProcessInspectionFlagGenerator,
    "16_Hex_Hunting": HexHuntingFlagGenerator,
    "17_Nmap_Scanning": NmapScanFlagGenerator,
    "18_Pcap_Search": PcapSearchFlagGenerator,
}


# === Master Flag Generation Class ===
class FlagGenerationManager:
    def __init__(self, dry_run=False, mode="guided"):
        self.project_root = self.find_project_root()
        self.web_admin_dir = self.project_root / "web_version_admin"
        self.dryrun_dir = self.project_root / "dryrun_output"
        self.dry_run = dry_run
        self.mode = mode  # guided or solo

        # Set challenge directory and validation unlocks file based on mode
        if self.mode == "solo":
            self.challenges_dir = self.project_root / "challenges_solo"
            self.unlocks_file = self.web_admin_dir / "validation_unlocks_solo.json"
            self.challenge_list = ChallengeList(challenges_file=self.web_admin_dir / "challenges_solo.json")
        else:
            self.challenges_dir = self.project_root / "challenges"
            self.unlocks_file = self.web_admin_dir / "validation_unlocks.json"
            self.challenge_list = ChallengeList(challenges_file=self.web_admin_dir / "challenges.json")

        # Prepare unlock data structure
        self.validation_unlocks = {}

    @staticmethod
    def find_project_root():
        """Walk up from current directory until .ccri_ctf_root is found."""
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker. Are you inside the CTF folder?", file=sys.stderr)
        sys.exit(1)

    def prepare_backup(self):
        """Create a backup of the challenges.json."""
        backup_file = self.web_admin_dir / f"challenges_{self.mode}.json.bak"
        shutil.copy2(self.web_admin_dir / f"challenges_{self.mode}.json", backup_file)
        print(f"📦 Backup created: {backup_file.relative_to(self.project_root)}")

    def save_unlocks(self):
        """Save validation unlocks JSON."""
        with open(self.unlocks_file, "w", encoding="utf-8") as f:
            json.dump(self.validation_unlocks, f, indent=2)
        print(f"🔑 Unlock data saved: {self.unlocks_file.relative_to(self.project_root)}")

    def print_flag_report(self, real_flag, fake_flags):
        """Print real and fake flags for sanity checking."""
        print(f"   🏁 Real flag: {real_flag}")
        if fake_flags:
            for fake in fake_flags:
                print(f"   🎭 Fake flag: {fake}")

    def generate_flags(self):
        """Iterate through challenges and generate flags."""
        print(f"\n🌐 Generating flags for {self.mode.upper()} mode...")

        if self.dry_run:
            print("📝 Dry-run mode enabled: outputs will be written to 'dryrun_output/'\n")
            self.dryrun_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.prepare_backup()

        success_count = 0
        fail_count = 0

        for challenge in self.challenge_list.get_challenges():
            try:
                folder_name = Path(challenge.getFolder()).name
                target_folder = (
                    self.dryrun_dir / self.mode / folder_name
                    if self.dry_run
                    else self.challenges_dir / folder_name
                )

                # Create challenge folder if it doesn't exist (non-destructive)
                target_folder.mkdir(parents=True, exist_ok=True)

                print(f"🚀 Generating flag for {challenge.getId()}...")

                generator_cls = GENERATOR_CLASSES.get(challenge.getId())
                if generator_cls:
                    generator = generator_cls(mode=self.mode)  # Pass mode to generator

                    # Run flag generation
                    real_flag = generator.generate_flag(target_folder)
                    fake_flags = getattr(generator, "last_fake_flags", [])

                    # Gather unlock hints from the generator
                    unlock_data = getattr(generator, "metadata", {})

                    for attr in ["last_password", "last_zip_password", "last_subdomains", "last_ports"]:
                        value = getattr(generator, attr, None)
                        if value:
                            unlock_data[attr] = value

                    self.validation_unlocks[challenge.getId()] = unlock_data

                    # Print flag report
                    self.print_flag_report(real_flag, fake_flags)

                    if self.dry_run:
                        print(f"✅ [Dry-Run] {challenge.getId()}: Real flag = {real_flag}")
                        print(f"📂 Would write files to: {target_folder.relative_to(self.project_root)}\n")
                    else:
                        challenge.flag = real_flag
                        print(f"✅ {challenge.getId()}: Real flag = {real_flag}\n")

                    success_count += 1
                else:
                    print(f"⚠️ No generator found for {challenge.getId()}. Skipping.\n")
            except Exception as e:
                print(f"❌ ERROR in {challenge.getId()}: {e}\n")
                fail_count += 1

        if not self.dry_run:
            self.challenge_list.save_challenges()
            print(f"🎉 All flags generated and challenges_{self.mode}.json updated.")
            self.save_unlocks()

        print(f"\n📊 Summary ({self.mode.upper()}): {success_count} successful | {fail_count} failed")


# === Entry Point ===
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--dry-run", action="store_true", help="Generate flags without modifying JSON files")
        args = parser.parse_args()

        print("🌐 Which mode do you want to generate?")
        print("1️⃣ Guided mode only")
        print("2️⃣ Solo mode only")
        print("3️⃣ Both (Guided + Solo)")
        mode_choice = input("Enter 1, 2, or 3: ").strip()

        if not args.dry_run:
            confirm = input("⚠️ Do you want to run in dry-run mode? (y/N): ").strip().lower()
            if confirm == "y":
                args.dry_run = True

        if mode_choice == "1":
            FlagGenerationManager(dry_run=args.dry_run, mode="guided").generate_flags()
        elif mode_choice == "2":
            FlagGenerationManager(dry_run=args.dry_run, mode="solo").generate_flags()
        elif mode_choice == "3":
            for m in ["guided", "solo"]:
                FlagGenerationManager(dry_run=args.dry_run, mode=m).generate_flags()
        else:
            print("❌ Invalid choice. Exiting.")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        input("🔴 Press Enter to close...")
