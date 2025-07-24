#!/usr/bin/env python3

from pathlib import Path
import random
import subprocess
import sys
import shutil
from flag_generators.flag_helpers import FlagUtils


class MetadataFlagGenerator:
    """
    Generator for the Metadata challenge.
    Embeds real and fake flags into EXIF metadata of capybara.jpg.
    Stores unlock metadata but leaves writing to master script.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo
        self.generator_dir = Path(__file__).parent.resolve()
        self.source_image = self.generator_dir / "capybara.jpg"
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

    def safe_cleanup(self, challenge_folder: Path):
        """Remove capybara.jpg and exiftool backup if present."""
        dest_image = challenge_folder / "capybara.jpg"
        backup_file = dest_image.with_suffix(dest_image.suffix + "_original")

        for file in [dest_image, backup_file]:
            if file.exists():
                try:
                    file.unlink()
                    print(f"🗑️ Removed old file: {file.relative_to(self.project_root)}")
                except Exception as e:
                    print(f"⚠️ Could not delete {file.name}: {e}", file=sys.stderr)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """Copy capybara.jpg and embed flags into EXIF metadata."""
        dest_image = challenge_folder / "capybara.jpg"

        if shutil.which("exiftool") is None:
            print("❌ exiftool is not installed.", file=sys.stderr)
            sys.exit(1)

        challenge_folder.mkdir(parents=True, exist_ok=True)
        self.safe_cleanup(challenge_folder)

        try:
            if not self.source_image.exists():
                raise FileNotFoundError(f"❌ Source image not found: {self.source_image}")
            dest_image.write_bytes(self.source_image.read_bytes())
            print(f"📂 Copied {self.source_image.name} to {challenge_folder.relative_to(self.project_root)}")
        except Exception as e:
            print(f"❌ Failed to copy image: {e}", file=sys.stderr)
            sys.exit(1)

        random.shuffle(fake_flags)
        metadata_tags = {
            "ImageDescription": fake_flags[0],
            "Artist": fake_flags[1],
            "Copyright": fake_flags[2],
            "XPKeywords": fake_flags[3],
            "UserComment": real_flag  # Real flag
        }

        print("📝 Embedding flags into EXIF metadata...")
        try:
            for tag, value in metadata_tags.items():
                subprocess.run(
                    ["exiftool", f"-{tag}={value}", str(dest_image)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True
                )
        except subprocess.CalledProcessError as e:
            print(f"❌ exiftool failed: {e.stderr.strip()}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error while embedding metadata: {e}", file=sys.stderr)
            sys.exit(1)

        backup_file = dest_image.with_suffix(dest_image.suffix + "_original")
        if backup_file.exists():
            try:
                backup_file.unlink()
                print("🗑️ Cleaned up exiftool backup file.")
            except Exception as e:
                print(f"⚠️ Could not remove backup file: {e}", file=sys.stderr)

        print(f"🎭 Fake flags: {', '.join(fake_flags)}")
        print(f"✅ Embedded real flag in UserComment: {real_flag}")

        # Store unlock metadata
        self.metadata = {
            "real_flag": real_flag,
            "challenge_file": str(dest_image.relative_to(self.project_root)),
            "unlock_method": "Inspect EXIF metadata of capybara.jpg to find the flag",
            "hint": "Use exiftool or exifread to view metadata tags."
        }

    def generate_flag(self, challenge_folder: Path) -> str:
        """Generate flags, embed them in metadata, and return the real flag."""
        real_flag = FlagUtils.generate_real_flag().replace("CCRI-", "CCRI-META-")

        fake_flags = set()
        attempts = 0
        while len(fake_flags) < 4:
            fake = FlagUtils.generate_fake_flag().replace("CCRI-", "FAKE-")
            if fake != real_flag:
                fake_flags.add(fake)
            attempts += 1
            if attempts > 1000:
                raise RuntimeError("❌ Too many attempts generating unique fake flags.")
        fake_flags = list(fake_flags)

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
