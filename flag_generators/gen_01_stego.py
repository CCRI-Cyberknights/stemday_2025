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
    """
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()
        self.generator_dir = self.project_root / "flag_generators"
        self.source_image = self.generator_dir / "squirrel.jpg"

        # === Exported unlock data for validation ===
        self.last_password = None
        self.last_fake_flags = []

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

    def safe_cleanup(self, challenge_folder: Path):
        """
        Remove only generated assets from the challenge folder.
        """
        for filename in ["squirrel.jpg", "hidden_flags.txt"]:
            target = challenge_folder / filename
            if target.exists():
                try:
                    target.unlink()
                    print(f"🗑️ Removed old file: {filename}")
                except Exception as e:
                    print(f"⚠️ Could not delete {filename}: {e}", file=sys.stderr)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list, passphrase="password"):
        """
        Copy pristine squirrel.jpg into the challenge folder and embed real + fake flags.
        """
        dest_image = challenge_folder / "squirrel.jpg"
        hidden_file = challenge_folder / "hidden_flags.txt"

        # Clean up only our generated assets
        self.safe_cleanup(challenge_folder)

        try:
            if not self.source_image.exists():
                raise FileNotFoundError(
                    f"❌ Source image not found: {self.source_image.relative_to(self.project_root)}"
                )

            # Copy clean squirrel.jpg into challenge folder
            dest_image.write_bytes(self.source_image.read_bytes())
            print(f"📂 Copied {self.source_image.name} to {challenge_folder.relative_to(self.project_root)}")

            # Combine and shuffle flags
            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)
            hidden_file.write_text("\n".join(all_flags))
            print(f"📝 Hidden flags saved to temporary file: {hidden_file.name}")

            # Embed flags with steghide
            print(f"🛠️ Embedding flags into {dest_image.name} using steghide...")
            subprocess.run([
                "steghide", "embed",
                "-cf", str(dest_image),
                "-ef", str(hidden_file),
                "-p", passphrase
            ], check=True)
            print(f"✅ Steghide embedding complete for {challenge_folder.name}")

        except FileNotFoundError as fnf_error:
            print(fnf_error)
            sys.exit(1)
        except subprocess.CalledProcessError as steghide_error:
            print(f"❌ Steghide failed with error: {steghide_error}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)
        finally:
            # Cleanup temp file
            if hidden_file.exists():
                try:
                    hidden_file.unlink()
                    print(f"🗑️ Cleaned up temporary file: {hidden_file.name}")
                except Exception as cleanup_error:
                    print(f"⚠️ Failed to delete {hidden_file.name}: {cleanup_error}")

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate a real flag, embed it into challenge_folder, and return plaintext flag.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]
        self.last_fake_flags = fake_flags  # Store for validation
        self.last_password = "password"   # Store password used

        self.embed_flags(challenge_folder, real_flag, fake_flags, passphrase=self.last_password)
        print('   🎭 Fake flags:', ', '.join(fake_flags))

        print(f"✅ Admin flag: {real_flag}")
        return real_flag
