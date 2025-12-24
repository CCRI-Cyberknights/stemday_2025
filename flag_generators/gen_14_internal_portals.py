#!/usr/bin/env python3

from pathlib import Path
import random
import sys
import json
import base64
from flag_generators.flag_helpers import FlagUtils

class InternalPortalFlagGenerator:
    """
    Generator for the Internal Portals challenge.
    Produces a hidden .server_data file containing HTML for 5 virtual internal sites.
    Web server reads this to serve pages at /internal/<site>.
    """

    # Renamed from SUBDOMAINS to PORTALS
    PORTALS = [
        ("alpha.cryptkeepers.local", "Alpha Service Portal", "Alpha Service", "Welcome to the Alpha team portal. All systems operational."),
        ("beta.cryptkeepers.local", "Beta Operations Dashboard", "Beta Operations", "Restricted Access – CryptKeepers only."),
        ("gamma.cryptkeepers.local", "Gamma Data API", "Gamma Data API", "Status: Maintenance Mode"),
        ("delta.cryptkeepers.local", "Delta API Service", "Delta API", "REST API Portal for Internal CryptKeepers use only."),
        ("omega.cryptkeepers.local", "Omega Internal Tools", "Omega Tools Suite", "For internal testing, staging and deployment.")
    ]

    FOOTERS = [
        "Alpha Service © 2025 CryptKeepers Network",
        "Beta Dashboard – CryptKeepers Internal Systems",
        "© 2025 CryptKeepers Network – Gamma Team",
        "Delta Service © CryptKeepers DevOps",
        "Omega Tools © CryptKeepers Engineering"
    ]

    ALT_DESCRIPTIONS = [
        "System running in nominal state.",
        "All services operational.",
        "Internal use only. Contact an on-call CryptKeeper for access.",
        "REST API endpoints active and monitored.",
        "Scheduled maintenance ongoing. Expect delays.",
    ]

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
        return Path.cwd()

    def generate_hidden_comment(self, flag: str) -> str:
        """Generates the flag hidden inside an HTML comment."""
        templates = [
            f"",
            f"",
            f"",
            f""
        ]
        return random.choice(templates)

    def create_html(self, portal_dns: str, title: str, header_title: str, header_desc: str, footer: str, flag: str, is_real: bool) -> str:
        alt_desc = random.choice(self.ALT_DESCRIPTIONS) if random.random() < 0.4 else header_desc
        
        # If this is the real flag, hide it in a comment.
        # If it's a fake flag, we also hide it in a comment so they have to check all pages!
        flag_comment = self.generate_hidden_comment(flag)

        # We inject the comment randomly in the HTML structure
        position = random.choice(["header", "main", "footer"])
        
        header_extra = flag_comment if position == "header" else ""
        main_extra = flag_comment if position == "main" else ""
        footer_extra = flag_comment if position == "footer" else ""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ font-family: sans-serif; background: #f4f4f9; padding: 2rem; }}
    header, footer {{ text-align: center; margin-bottom: 2rem; color: #555; }}
    main {{ background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }}
    h1 {{ color: #333; }}
    .status {{ background: #eef; padding: 10px; border-left: 4px solid #4a90e2; margin-top: 20px; }}
  </style>
</head>
<body>
  <header>
    <h1>{header_title}</h1>
    <p>{alt_desc}</p>
    {header_extra}
  </header>

  <main>
    <section>
      <h2>System Status</h2>
      <p>Operational. All nodes online.</p>
      <div class="status">
        <strong>Metric:</strong> {random.randint(90, 100)}% uptime.
      </div>
      {main_extra}
    </section>
  </main>

  <footer>
    <hr>
    <p>{footer}</p>
    <p><small>Internal Access Only - {portal_dns}</small></p>
    {footer_extra}
  </footer>
</body>
</html>"""

    def clean_previous_data(self, challenge_folder: Path):
        server_data_file = challenge_folder / ".server_data"
        if server_data_file.exists():
            try:
                server_data_file.unlink()
            except Exception as e:
                print(f"⚠️ Could not delete {server_data_file.name}: {e}", file=sys.stderr)

        # Remove legacy html files to force use of web server
        for old_file in challenge_folder.glob("*.html"):
            try:
                old_file.unlink()
            except: 
                pass

    def embed_data(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        try:
            challenge_folder.mkdir(parents=True, exist_ok=True)
            self.clean_previous_data(challenge_folder)

            flags = fake_flags + [real_flag]
            random.shuffle(flags)

            server_data = {}

            # Updated loop to use self.PORTALS
            for (portal_dns, title, header_title, header_desc), footer, flag in zip(
                self.PORTALS, self.FOOTERS, flags
            ):
                is_real = (flag == real_flag)
                html_content = self.create_html(portal_dns, title, header_title, header_desc, footer, flag, is_real)
                
                # Extract the "short name" for the web route (e.g., "alpha" from "alpha.cryptkeepers.local")
                short_name = portal_dns.split('.')[0]
                server_data[short_name] = html_content

                if is_real:
                    print(f"✅ Flag hidden in source of: {short_name} ({portal_dns})")

            # Obfuscate / Encode data
            json_str = json.dumps(server_data)
            b64_data = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

            target_file = challenge_folder / ".server_data"
            target_file.write_text(b64_data)
            print(f"💾 Saved web server configuration to {target_file.relative_to(self.project_root)}")

            self.metadata = {
                "real_flag": real_flag,
                "challenge_folder": str(challenge_folder.relative_to(self.project_root)),
                "unlock_method": "Inspect HTML Source Code (View Source) of internal portals.",
                "hint": "Look for in the source."
            }

        except Exception as e:
            print(f"❌ Failed during Internal Portals generation: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = list({FlagUtils.generate_fake_flag() for _ in range(4)})

        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_data(challenge_folder, real_flag, fake_flags)
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag