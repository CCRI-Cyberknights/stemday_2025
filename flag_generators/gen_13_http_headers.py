#!/usr/bin/env python3

from pathlib import Path
import random
import sys
import json
import base64
from flag_generators.flag_helpers import FlagUtils

class HTTPHeaderFlagGenerator:
    """
    Generator for the HTTP Headers challenge.
    Produces a hidden .server_data file containing configuration for 5 endpoints.
    Web server reads this to serve responses.
    """

    SERVERS = [
        "CryptKeepers-Gateway/2.3.1", "CryptKeepers-Node/3.0.0-beta",
        "Apache/2.4.54 (Ubuntu)", "nginx/1.24.0", "Go HTTP Server/1.19"
    ]

    POWERED_BY = [
        "PHP/8.1.12", "Python/3.11.4", "Node.js/18.16.0", 
        "ASP.NET Core/7.0", "Ruby on Rails/7.1.0"
    ]

    CONTENT_TYPES = [
        "text/html; charset=UTF-8", "application/json", "text/plain; charset=UTF-8",
    ]

    CACHE_CONTROLS = [
        "no-store", "public, max-age=86400", "private, no-cache"
    ]

    HTML_BODIES = [
        "<html><head><title>Portal</title></head><body><h1>CryptKeepers Hub</h1><p>System maintenance active.</p></body></html>",
        "<html><head><title>Dashboard</title></head><body><h1>Ops Dashboard</h1><p>Redirecting...</p></body></html>",
        "<html><head><title>Data</title></head><body><h1>Data Service</h1><p>Ready.</p></body></html>",
        "{\"status\": \"ok\", \"message\": \"API v1.2.4\", \"notes\": \"Nominal\"}",
        "CryptKeepers plain text endpoint. Status: OK"
    ]

    HTML_COMMENTS = [
        "", "",
        "", "",
        ""
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
        # Fallback if marker not found
        return Path.cwd()

    def generate_endpoint_data(self, flag: str) -> dict:
        """Creates the headers and body for a single endpoint."""
        headers = {
            "Server": random.choice(self.SERVERS),
            "Content-Type": random.choice(self.CONTENT_TYPES),
            "Cache-Control": random.choice(self.CACHE_CONTROLS),
            "X-Powered-By": random.choice(self.POWERED_BY),
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff"
        }
        
        # Add the flag header
        headers["X-Flag"] = flag

        if random.random() < 0.6:
            session_id = ''.join(random.choices("abcdef0123456789", k=16))
            headers["Set-Cookie"] = f"sessionid={session_id}; HttpOnly; Secure"

        body = random.choice(self.HTML_BODIES) + "\n" + random.choice(self.HTML_COMMENTS)
        
        return {
            "headers": headers,
            "body": body,
            "status_code": 200
        }

    def clean_previous_data(self, challenge_folder: Path):
        """Removes old artifacts to ensure a clean generation."""
        server_data_file = challenge_folder / ".server_data"
        if server_data_file.exists():
            try:
                server_data_file.unlink()
                # print(f"🗑️ Removed old server configuration.") 
            except Exception as e:
                print(f"⚠️ Could not delete {server_data_file.name}: {e}", file=sys.stderr)

    def embed_data(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        try:
            challenge_folder.mkdir(parents=True, exist_ok=True)
            
            # clean up both .server_data
            self.clean_previous_data(challenge_folder)

            all_flags = fake_flags + [real_flag]
            random.shuffle(all_flags)

            server_data = {}

            # Generate data for 5 endpoints
            for i, flag in enumerate(all_flags, start=1):
                endpoint_key = f"endpoint_{i}"
                data = self.generate_endpoint_data(flag)
                server_data[endpoint_key] = data
                
                if flag == real_flag:
                    print(f"✅ Flag hidden in {endpoint_key}")

            # Obfuscate / Encode data so it's not readable in plain text
            json_str = json.dumps(server_data)
            b64_data = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

            # Save to hidden file
            target_file = challenge_folder / ".server_data"
            target_file.write_text(b64_data)
            print(f"💾 Saved web server configuration to {target_file.relative_to(self.project_root)}")

            self.metadata = {
                "real_flag": real_flag,
                ""challenge_file": str(target_file.relative_to(self.project_root)),
                "unlock_method": "Use curl -I to check headers of /mystery/endpoint_X",
                "hint": "Check X-Flag header"
            }

        except Exception as e:
            print(f"❌ Failed during HTTP response generation: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = list({FlagUtils.generate_fake_flag() for _ in range(4)})
        while real_flag in fake_flags:
            real_flag = FlagUtils.generate_real_flag()

        self.embed_data(challenge_folder, real_flag, fake_flags)
        print(f"✅ {self.mode.capitalize()} flag: {real_flag}")
        return real_flag