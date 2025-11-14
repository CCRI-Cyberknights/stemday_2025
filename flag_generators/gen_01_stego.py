#!/usr/bin/env python3

from pathlib import Path
import subprocess
import random
import sys
from flag_generators.flag_helpers import FlagUtils


class StegoFlagGenerator:
    """
    Generator for the Stego challenge flags.
    Embeds real and fake flags into a squirrel.jpg image using steghide.
    Behavior adapts based on 'guided' or 'solo' mode.
    """

    def __init__(self, project_root: Path = None, mode: str = "guided"):
        self.project_root = project_root or self.find_project_root()
        self.generator_dir = self.project_root / "flag_generators"
        self.source_image = self.generator_dir / "squirrel.jpg"
        self.mode = mode.lower()

        if self.mode not in ["guided", "solo"]:
            print(f"❌ ERROR: Invalid mode '{self.mode}'. Expected 'guided' or 'solo'.", file=sys.stderr)
            sys.exit(1)

        # Exported for validation metadata
        self.last_password = None
        self.last_fake_flags = []
        self.metadata = {}  # Optional: additional future unlock data

    @staticmethod
    def find_project_root() -> Path:
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find project root marker (.ccri_ctf_root).", file=sys.stderr)
        sys.exit(1)

    def safe_cleanup(self, challenge_folder: Path):
        for filename in ["squirrel.jpg", "hidden_flags.txt"]:
            target = challenge_folder / filename
            if target.exists():
                try:
                    target.unlink()
                    print(f"🗑️ Removed old file: {filename}")
                except Exception as e:
                    print(f"⚠️ Could not delete {filename}: {e}", file=sys.stderr)

    def write_password_metadata(self, image_path: Path, passphrase: str):
        """
        Add a mode-specific hint into the JPEG metadata using exiftool.

        - guided: very explicit hint with the word 'password'
        - solo: CryptKeeper-themed hint that still contains the actual passphrase
        """
        if self.mode == "guided":
            comment = f"Guided hint: steghide passphrase is '{passphrase}'."
        else:
            # CryptKeeper-themed but still exposes the word, so metadata matters
            comment = (
                "CryptKeepers are creatures of habit. "
                f'The key they whisper is "{passphrase}".'
            )

        try:
            subprocess.run(
                [
                    "exiftool",
                    "-overwrite_original",
                    f"-UserComment={comment}",
                    str(image_path),
                ],
                check=True,
            )
            print("📝 Embedded password hint into JPEG metadata (UserComment).")
        except FileNotFoundError:
            print("⚠️ exiftool not found; skipping metadata hint.", file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ exiftool failed: {e}", file=sys.stderr)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list, passphrase: str):
        dest_image = challenge_folder / "squirrel.jpg"
        hidden_file = challenge_folder / "hidden_flags.txt"
        self.safe_cleanup(challenge_folder)

        try:
            if not self.source_image.exists():
                raise FileNotFoundError(f"❌ Source image not found: {self.source_image.relative_to(self.project_root)}")

            # Copy clean source image
            dest_image.write_bytes(self.source_image.read_bytes())
            print(f"📂 Copied {self.source_image.name} to {challenge_folder.relative_to(self.project_root)}")

            # Build payload of real + fake flags
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)
            hidden_file.write_text("\n".join(all_flags))
            print(f"📝 Hidden flags saved to temporary file: {hidden_file.name}")

            MAX_PAYLOAD = 2000
            if hidden_file.stat().st_size > MAX_PAYLOAD:
                print(f"⚠️ Payload too large. Falling back to real flag only.")
                hidden_file.write_text(real_flag)

            # Embed with steghide
            subprocess.run([
                "steghide", "embed",
                "-cf", str(dest_image),
                "-ef", str(hidden_file),
                "-p", passphrase
            ], check=True)
            print(f"✅ Steghide embedding complete for {challenge_folder.name}")

            # Add metadata *after* embedding so it survives
            self.write_password_metadata(dest_image, passphrase)

        except Exception as e:
            print(f"❌ ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            if hidden_file.exists():
                try:
                    hidden_file.unlink()
                    print(f"🗑️ Cleaned up temporary file: {hidden_file.name}")
                except Exception as e:
                    print(f"⚠️ Failed to delete {hidden_file.name}: {e}")

    def generate_flag(self, challenge_folder: Path) -> str:
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        self.last_fake_flags = fake_flags
        # 🔑 Different passwords per mode
        self.last_password = "password" if self.mode == "guided" else "ckeepers"

        # Build standardized metadata so the master script writes a rich unlock entry
        base_path = "challenges_solo" if self.mode == "solo" else "challenges"
        challenge_id = challenge_folder.name  # e.g., "01_Stego"
        challenge_file = f"{base_path}/{challenge_id}/squirrel.jpg"

        # Mode-specific hint: guided can be explicit, solo points at metadata
        if self.mode == "guided":
            hint = "Use: steghide extract -sf squirrel.jpg -p password"
        else:
            hint = "Check the JPEG metadata for a CryptKeeper-themed hint about the steghide passphrase."

        self.metadata = {
            "real_flag": real_flag,
            "challenge_file": challenge_file,
            "unlock_method": "steghide extract -sf squirrel.jpg -p <password>",
            "hint": hint,
            "last_password": self.last_password,
            # Optional but handy for audits:
            "fake_flags": fake_flags,
        }

        # Do the actual embedding
        self.embed_flags(challenge_folder, real_flag, fake_flags, passphrase=self.last_password)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ {self.mode.capitalize()} flag: {real_flag} (passphrase: {self.last_password})")
        return real_flag
