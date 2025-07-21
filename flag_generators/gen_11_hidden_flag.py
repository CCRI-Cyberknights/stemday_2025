#!/usr/bin/env python3

from pathlib import Path
import random
import shutil
import sys
import json
from flag_generators.flag_helpers import FlagUtils


class HiddenFlagGenerator:
    """
    Generator for the Hidden Flag challenge.
    Builds a fake folder structure and hides real + fake flags in random files.
    Supports guided and solo modes with separate unlock metadata.
    """

    FOLDERS_AND_FILES = {
        "backup": ["sysdump.bak", ".config.old"],
        "data": ["info.tmp", ".hint_file", ".summary"],
        "logs": ["old.log", ".keep.tmp", ".notes"],
        "ref": ["readme.txt", ".archive"],
    }

    FILE_BASED_JUNK = {
        "sysdump.bak": [
            "### System Memory Dump ###",
            "Heap analysis: no anomalies detected.",
            "Saved core dump for developer inspection.",
        ],
        ".config.old": [
            "# Legacy configuration file",
            "user=guest",
            "enable_logging=true",
            "last_modified=2019-08-12",
        ],
        "info.tmp": [
            "[INFO BLOCK]",
            "Session start: 2025-06-21 09:15",
            "Temporary cache: active",
            "User: ccri_admin",
        ],
        ".hint_file": [
            "# HINT: Sometimes things are not as they seem...",
            "Metadata may contain valuable information.",
            "Cross-check all hidden files carefully.",
        ],
        ".summary": [
            "=== Data Summary Report ===",
            "Total records processed: 1024",
            "Errors encountered: 0",
            "Exported successfully to archive.",
        ],
        "old.log": [
            "[2025-06-19 14:33:01] INFO User login attempt.",
            "[2025-06-19 14:34:11] DEBUG Connection established.",
            "[2025-06-19 14:35:22] WARN Disk usage at 92%.",
        ],
        ".keep.tmp": [
            "# Temporary Keep File",
            "Do not delete until verified by sysadmin.",
            "Checksum: a9b8c7d6e5f4",
        ],
        ".notes": [
            "Research notes for backup procedures.",
            "Remember to check permissions after restore.",
            "TODO: Document encryption key rotation.",
        ],
        "readme.txt": [
            "Welcome to the reference directory.",
            "This folder contains assorted documentation.",
            "Review each file carefully.",
        ],
        ".archive": [
            "# Archive header",
            "Compression method: gzip",
            "Created by archiver v2.1",
        ],
    }

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

    def safe_cleanup(self, base_dir: Path):
        """
        Clean up only the 'junk/' subfolder if it exists.
        """
        if base_dir.exists():
            print(f"🗑️ Removing old folder: {base_dir.relative_to(self.project_root)}")
            try:
                shutil.rmtree(base_dir)
            except Exception as e:
                print(f"⚠️ Could not delete {base_dir.name}: {e}", file=sys.stderr)

    def generate_junk_for_file(self, file_name: str, flag: str = None) -> str:
        """
        Generate 3–7 lines of junk text for the specific file name,
        optionally embedding a flag.
        """
        snippets = self.FILE_BASED_JUNK.get(file_name, ["# Generic placeholder content"])
        lines = random.choices(snippets, k=random.randint(3, 7))
        insert_pos = random.randint(0, len(lines))
        lines.insert(insert_pos, flag if flag else "# [No sensitive data found here]")
        return "\n".join(lines)

    def create_folder_structure(self, base_dir: Path, real_flag: str, fake_flags: list):
        """
        Build the fixed folder structure and embed flags randomly in files.
        """
        self.safe_cleanup(base_dir)

        try:
            base_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"❌ Failed to prepare folder structure: {e}", file=sys.stderr)
            sys.exit(1)

        all_files = []
        for folder_name, files in self.FOLDERS_AND_FILES.items():
            folder_path = base_dir / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            for file_name in files:
                file_path = folder_path / file_name
                all_files.append(file_path)

        # Randomly select 5 files for flags
        flag_files = random.sample(all_files, 5)
        real_flag_file = flag_files[0]
        fake_flag_files = flag_files[1:]

        print(f"🎭 Fake flags: {', '.join(fake_flags)}")

        for file_path in all_files:
            try:
                if file_path == real_flag_file:
                    content = self.generate_junk_for_file(file_path.name, real_flag)
                elif file_path in fake_flag_files:
                    fake_flag = fake_flags.pop()
                    content = self.generate_junk_for_file(file_path.name, fake_flag)
                else:
                    content = self.generate_junk_for_file(file_path.name)
                file_path.write_text(content)
            except Exception as e:
                print(f"❌ Failed to write to {file_path.relative_to(self.project_root)}: {e}", file=sys.stderr)

        print(f"✅ Real flag hidden in: {real_flag_file.relative_to(base_dir)}")
        print("📁 Folder structure created with embedded flags.")

        # Record unlock metadata
        try:
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            unlocks["11_HiddenFlag"] = {
                "real_flag": real_flag,
                "challenge_folder": str(base_dir.relative_to(self.project_root)),
                "unlock_method": "Search recursively for the flag in hidden files",
                "hint": "Use grep -R or find/strings to locate the flag in junk/"
            }

            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved to: {self.unlock_file.relative_to(self.project_root)}")

        except Exception as e:
            print(f"❌ Failed to update {self.unlock_file.name}: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate the fixed folder structure with 1 real + 4 fake flags,
        and return the real flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.create_folder_structure(challenge_folder / "junk", real_flag, fake_flags)
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
