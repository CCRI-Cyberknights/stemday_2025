#!/usr/bin/env python3

from pathlib import Path
import random
import sys
import json
from flag_generators.flag_helpers import FlagUtils


class SubdomainSweepFlagGenerator:
    """
    Generator for the Subdomain Sweep challenge.
    Produces 5 subdomain HTML files with 1 real flag and 4 decoys.
    Supports guided and solo modes.
    """

    SUBDOMAINS = [
        ("alpha.liber8.local", "Alpha Service Portal", "Alpha Service", "Welcome to the Alpha team portal. All systems operational."),
        ("beta.liber8.local", "Beta Operations Dashboard", "Beta Operations", "Restricted Access – Authorized Personnel Only"),
        ("gamma.liber8.local", "Gamma Data API", "Gamma Data API", "Status: Maintenance Mode"),
        ("delta.liber8.local", "Delta API Service", "Delta API", "REST API Portal for Internal Use Only"),
        ("omega.liber8.local", "Omega Internal Tools", "Omega Tools Suite", "For Internal Testing and Deployment")
    ]

    FOOTERS = [
        "Alpha Service © 2025 Liber8 Network",
        "Beta Dashboard – Liber8 Internal Systems",
        "© 2025 Liber8 Network – Gamma Team",
        "Delta Service © Liber8 DevOps",
        "Omega Tools © Liber8 Engineering"
    ]

    ALT_DESCRIPTIONS = [
        "System running in nominal state.",
        "All services operational.",
        "Internal use only. Contact admin for access.",
        "REST API endpoints active and monitored.",
        "Scheduled maintenance ongoing. Expect delays."
    ]

    ALT_PRE_LINES = [
        "[INFO] Service heartbeat received.",
        "[DEBUG] Connection pool warmed up.",
        "[TRACE] User session started: {}",
        "[WARN] Unexpected response code: 503",
        "[INFO] Scheduled job completed successfully.",
        "[DEBUG] Cache cleared for /api/v1/resources.",
        "[NOTICE] Authentication handshake completed."
    ]

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.mode = mode  # guided or solo

        # Select unlock metadata file for this mode
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

    def generate_logs(self, flag: str) -> str:
        """Generate 3–5 log lines, embedding the flag in one randomly."""
        lines = random.sample(self.ALT_PRE_LINES, random.randint(3, 5))
        insert_pos = random.randint(0, len(lines) - 1)

        if '{}' in lines[insert_pos]:
            lines[insert_pos] = lines[insert_pos].format(flag)
        else:
            lines[insert_pos] = f"[TRACE] Embedded flag: {flag}"

        return "\n".join(lines)

    def embed_flag(self, flag: str) -> str:
        """Embed the flag in either a <p> or <pre> block."""
        if random.random() < 0.5:
            return f"<p><strong>Note:</strong> {flag}</p>"
        else:
            return f"<pre>\n{self.generate_logs(flag)}\n</pre>"

    def clean_old_subdomain_html(self, challenge_folder: Path):
        """Remove existing subdomain HTML files (*.liber8.local.html)."""
        if challenge_folder.exists():
            for file in challenge_folder.glob("*.liber8.local.html"):
                try:
                    file.unlink()
                    print(f"🗑️ Removed old file: {file.name}")
                except Exception as e:
                    print(f"⚠️ Could not delete {file.name}: {e}", file=sys.stderr)
        else:
            print(f"📁 Creating challenge folder: {challenge_folder.relative_to(self.project_root)}")
            challenge_folder.mkdir(parents=True, exist_ok=True)

    def update_validation_unlocks(self, real_flag: str, challenge_folder: Path):
        """Save metadata to the correct unlocks JSON."""
        try:
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            unlocks["14_SubdomainSweep"] = {
                "real_flag": real_flag,
                "challenge_folder": str(challenge_folder.relative_to(self.project_root)),
                "unlock_method": "Inspect HTML files for subdomains to locate the flag",
                "hint": "Search *.liber8.local.html for the flag string using grep or a browser"
            }

            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved to: {self.unlock_file.relative_to(self.project_root)}")

        except Exception as e:
            print(f"❌ Failed to update {self.unlock_file.name}: {e}", file=sys.stderr)
            sys.exit(1)

    def embed_subdomain_html(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """Generate HTML files for each subdomain."""
        self.clean_old_subdomain_html(challenge_folder)

        flags = fake_flags + [real_flag]
        random.shuffle(flags)

        print(f"🎭 Fake flags: {', '.join(fake_flags)}")

        for (subdomain, title, header_title, header_desc), footer, flag in zip(
            self.SUBDOMAINS, self.FOOTERS, flags
        ):
            file_path = challenge_folder / f"{subdomain}.html"
            html_content = self.create_html(subdomain, title, header_title, header_desc, footer, flag)
            file_path.write_text(html_content, encoding="utf-8")

            if flag == real_flag:
                print(f"✅ {file_path.name} (REAL flag)")
                real_file = file_path
            else:
                print(f"➖ {file_path.name} (decoy)")

        # Save unlock metadata
        self.update_validation_unlocks(real_flag, challenge_folder)

    def create_html(self, subdomain: str, title: str, header_title: str, header_desc: str, footer: str, flag: str) -> str:
        """Generate randomized HTML content for a subdomain."""
        alt_desc = random.choice(self.ALT_DESCRIPTIONS) if random.random() < 0.4 else header_desc
        flag_block = self.embed_flag(flag)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
</head>
<body>
  <header>
    <h1>{header_title}</h1>
    <p>{alt_desc}</p>
  </header>

  <main>
    <section>
      <h2>Recent Activity</h2>
      {flag_block}
    </section>

    <section>
      <h2>Status</h2>
      <p>{alt_desc}</p>
    </section>
  </main>

  <footer>
    <p>{footer}</p>
  </footer>
</body>
</html>"""

    def generate_flag(self, challenge_folder: Path) -> str:
        """Generate subdomain HTML files and return the real flag."""
        real_flag = FlagUtils.generate_real_flag()

        fake_flags = list({FlagUtils.generate_fake_flag() for _ in range(4)})

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_subdomain_html(challenge_folder, real_flag, fake_flags)
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag
