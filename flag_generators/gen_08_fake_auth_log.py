#!/usr/bin/env python3

from pathlib import Path
import random
import datetime
import sys
from flag_generators.flag_helpers import FlagUtils


class FakeAuthLogFlagGenerator:
    """
    Generator for the Fake Auth Log challenge.
    Embeds real and fake flags into a simulated auth.log file.
    Collects metadata for the master script to handle unlocks.json.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo
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
        """Remove previously generated auth.log file."""
        log_file = challenge_folder / "auth.log"
        if log_file.exists():
            try:
                log_file.unlink()
                print(f"🗑️ Removed old file: {log_file.relative_to(self.project_root)}")
            except Exception as e:
                print(f"⚠️ Could not delete {log_file.name}: {e}", file=sys.stderr)

    def embed_flags(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Generate a fake auth.log file with real and fake flags embedded as PIDs.
        Solo mode adds more noise for extra difficulty.
        """
        try:
            self.safe_cleanup(challenge_folder)
            challenge_folder.mkdir(parents=True, exist_ok=True)
            log_path = challenge_folder / "auth.log"

            usernames = ["alice", "bob", "charlie", "dave", "eve"]
            ip_addresses = [
                "192.168.1.10", "192.168.1.20", "10.0.0.5", "172.16.0.3",
                "203.0.113.42", "198.51.100.17", "192.0.2.91", "8.8.8.8", "127.0.0.1"
            ]
            auth_methods = ["password", "publickey"]

            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            line_count = 400 if self.mode == "solo" else 250
            fail_ratio = 0.6 if self.mode == "solo" else 0.2

            base_time = datetime.datetime.now()
            flag_insertion_indices = sorted(random.sample(range(50, line_count - 20), len(all_flags)))
            flag_index = 0
            lines = []

            for i in range(line_count):
                timestamp = (base_time - datetime.timedelta(seconds=random.randint(0, 7200))).strftime("%b %d %H:%M:%S")
                user = random.choice(usernames)
                ip = random.choice(ip_addresses)
                method = random.choice(auth_methods)
                result = "Accepted" if random.random() > fail_ratio else "Failed"

                if flag_index < len(flag_insertion_indices) and i == flag_insertion_indices[flag_index]:
                    pid = all_flags[flag_index]
                    flag_index += 1
                else:
                    pid = str(random.randint(1000, 99999))

                line = f"{timestamp} myhost sshd[{pid}]: {result} {method} for {user} from {ip} port {random.randint(1000, 65000)} ssh2"
                lines.append(line)

            log_path.write_text("\n".join(lines))
            print(f"📝 Fake auth.log created: {log_path.relative_to(self.project_root)}")

            # Save metadata for master script
            self.metadata = {
                "real_flag": real_flag,
                "reconstructed_flag": real_flag,
                "challenge_file": str(log_path.relative_to(self.project_root)),
                "unlock_method": "Inspect auth.log for embedded flag in sshd PIDs",
                "hint": "Look for unusual process IDs in auth.log to spot the flag."
            }

        except PermissionError:
            print(f"❌ Permission denied: Cannot write to {log_path.relative_to(self.project_root)}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"💥 Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """Generate real and fake flags, embed them, and return the real one."""
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = [FlagUtils.generate_fake_flag() for _ in range(4)]

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_flags(challenge_folder, real_flag, fake_flags)
        print('   🎭 Fake flags:', ', '.join(fake_flags))
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
