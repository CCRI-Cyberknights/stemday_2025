#!/usr/bin/env python3

from pathlib import Path
import random
import sys
import json
import base64
from flag_generators.flag_helpers import FlagUtils

class InternalPortalFlagGenerator:
    """
    Challenge 14 Generator: DOM-Injection Edition.
    Avoids HTML comments to prevent environment-based stripping.
    """

    def __init__(self, project_root: Path = None, mode="guided"):
        self.project_root = project_root or Path.cwd()
        self.mode = mode
        self.metadata = {}

    def get_template(self, title, desc, flag, domain):
        # We use direct string concatenation to be 100% safe
        html = "<!DOCTYPE html>\n<html>\n<head>\n"
        html += "  <meta charset='UTF-8'>\n"
        html += "  <title>" + str(title) + "</title>\n"
        html += "  <style>body { font-family: monospace; padding: 2rem; }</style>\n"
        html += "</head>\n<body>\n"
        html += "  <h1>" + str(title) + "</h1>\n"
        html += "  <p>" + str(desc) + "</p>\n"
        html += "  <hr>\n"
        
        # INJECTION: Using a hidden span instead of a comment
        # This is harder for environment 'cleaners' to strip
        html += "  <span style='display:none' id='debug-info'>Flag: " + str(flag) + "</span>\n"
        
        html += "  <p>System ID: " + str(domain) + "</p>\n"
        html += "</body>\n</html>"
        
        # Immediate Forensic Check
        if str(flag) not in html:
            print(f"\nFATAL: Flag {flag} still not in string after concatenation!")
            sys.exit(1)
            
        return html

    def generate_flag(self, challenge_folder: Path) -> str:
        real_flag = FlagUtils.generate_real_flag()
        fakes = [FlagUtils.generate_fake_flag() for _ in range(4)]
        all_flags = fakes + [real_flag]
        random.shuffle(all_flags)
        
        portals = [
            ("alpha", "Alpha Service", "All systems operational."),
            ("beta",  "Beta Dashboard", "Restricted Access."),
            ("gamma", "Gamma API",      "Maintenance Mode."),
            ("delta", "Delta Service",  "API Online."),
            ("omega", "Omega Tools",    "Internal Testing.")
        ]

        server_data = {}
        for i, (name, title, desc) in enumerate(portals):
            current_flag = all_flags[i]
            server_data[name] = self.get_template(title, desc, current_flag, name)
            if current_flag == real_flag:
                print(f"DEBUG: Real flag assigned to {name}")

        # Write to Disk
        challenge_folder.mkdir(parents=True, exist_ok=True)
        target_file = challenge_folder / '.server_data'
        
        raw_json = json.dumps(server_data)
        b64_data = base64.b64encode(raw_json.encode('utf-8')).decode('utf-8')
        target_file.write_text(b64_data, encoding='utf-8')

        self.metadata = {
            "real_flag": real_flag,
            "challenge_folder": str(challenge_folder),
            "unlock_method": "Inspect DOM / View Source",
            "hint": "Check hidden span elements"
        }
        
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag