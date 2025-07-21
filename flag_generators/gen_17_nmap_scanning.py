#!/usr/bin/env python3

import random
import re
import sys
import json
from pathlib import Path
from flag_generators.flag_helpers import FlagUtils


class NmapScanFlagGenerator:
    """
    Generator for the Nmap Scanning challenge.
    Dynamically patches web_version_admin/server.py with random ports,
    flags, and service names for realism.
    Stores unlock metadata for validation workflow.
    """

    def __init__(self, project_root: Path = None, server_file: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.server_file = server_file or self.project_root / "web_version_admin" / "server.py"
        self.mode = mode  # guided or solo

        # Choose port range based on mode
        self.port_range = (
            list(range(8000, 8100)) if self.mode == "guided" else list(range(9000, 9100))
        )

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

    def random_ports(self, port_range, exclude_ports, count):
        """Pick unique random ports from a range, excluding certain ports."""
        available = set(port_range) - set(exclude_ports)
        return random.sample(sorted(available), count)

    def patch_server_file(self, real_flag: str, fake_flags: dict, real_port: int, junk_ports: dict):
        """Update FAKE_FLAGS and SERVICE_NAMES in server.py with randomized ports, flags, and service names."""
        server_file = self.server_file.resolve()

        if not server_file.exists():
            print(f"❌ ERROR: {server_file} not found.", file=sys.stderr)
            sys.exit(1)

        try:
            # === Random service names for all open ports ===
            all_ports = [real_port] + list(fake_flags.keys()) + list(junk_ports.keys())
            service_name_pool = [
                "alpha-core", "delta-sync", "gamma-relay", "beta-hub",
                "lambda-api", "omega-stream", "theta-daemon", "epsilon-sync",
                "kappa-node", "zeta-cache", "delta-proxy", "sysmon-api",
                "configd", "metricsd", "auth-service", "update-agent"
            ]
            random.shuffle(service_name_pool)
            combined_service_names = {}
            for i, port in enumerate(all_ports):
                combined_service_names[port] = service_name_pool[i % len(service_name_pool)]

            # === Build replacement FAKE_FLAGS block ===
            new_fake_flags = [f"    {real_port}: \"{real_flag}\",       # ✅ REAL FLAG"]
            for port, flag in fake_flags.items():
                new_fake_flags.append(f"    {port}: \"{flag}\",       # fake")
            new_fake_flags_block = "FAKE_FLAGS = {\n" + "\n".join(new_fake_flags) + "\n}"

            # === Build SERVICE_NAMES update block ===
            service_name_updates = [
                f"    {port}: \"{name}\"" for port, name in combined_service_names.items()
            ]
            new_service_names_block = (
                "SERVICE_NAMES.update({\n" +
                ",\n".join(service_name_updates) +
                "\n})"
            )

            # === Read server.py content
            print(f"📂 Reading {server_file}...")
            content = server_file.read_text(encoding="utf-8")

            # === Replace FAKE_FLAGS block
            new_content, count_flags = re.subn(
                r"FAKE_FLAGS\s*=\s*\{[^}]*\}",
                new_fake_flags_block,
                content,
                flags=re.DOTALL
            )
            if count_flags == 0:
                raise RuntimeError("No FAKE_FLAGS block found to replace!")

            # === Replace or Insert SERVICE_NAMES.update block
            new_content, count_names = re.subn(
                r"SERVICE_NAMES\.update\(\s*\{[^}]*\}\s*\)",
                new_service_names_block,
                new_content,
                flags=re.DOTALL
            )
            if count_names == 0:
                # Insert update block after FAKE_FLAGS if not present
                new_content = new_content.replace(
                    "# Combine real flags and junk responses",
                    "# Combine real flags and junk responses\n" + new_service_names_block
                )

            # === Backup and write updated server.py
            backup_file = server_file.with_suffix(".bak")
            if not backup_file.exists():
                server_file.replace(backup_file)
                print(f"🗄️ Backup created: {backup_file.name}")
            else:
                print(f"🗄️ Backup already exists: {backup_file.name}")

            server_file.write_text(new_content, encoding="utf-8")
            print(f"✅ Updated {server_file.name}")

            # === Record unlock metadata
            self.metadata = {
                "real_flag": real_flag,
                "real_port": real_port,
                "server_file": str(server_file.relative_to(self.project_root)),
                "unlock_method": f"Scan ports {self.port_range[0]}-{self.port_range[-1]} and query HTTP endpoints to locate the real flag (port {real_port})",
                "hint": f"Use nmap -p{self.port_range[0]}-{self.port_range[-1]} localhost to discover ports and curl to check flags."
            }

            # Save metadata
            self.update_validation_unlocks()

        except Exception as e:
            print(f"❌ ERROR during server.py patching: {e}", file=sys.stderr)
            sys.exit(1)

    def update_validation_unlocks(self):
        """Save metadata into validation_unlocks JSON for this mode."""
        try:
            if self.unlock_file.exists():
                with open(self.unlock_file, "r", encoding="utf-8") as f:
                    unlocks = json.load(f)
            else:
                unlocks = {}

            unlocks["17_Nmap_Scanning"] = self.metadata

            with open(self.unlock_file, "w", encoding="utf-8") as f:
                json.dump(unlocks, f, indent=2)
            print(f"💾 Metadata saved to: {self.unlock_file.relative_to(self.project_root)}")

        except Exception as e:
            print(f"❌ Failed to update {self.unlock_file.name}: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        """Generate real and fake flags, patch server.py, and return real flag."""
        # === Select random ports for flags ===
        selected_flag_ports = self.random_ports(self.port_range, [], 5)
        real_port = selected_flag_ports[0]
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = {port: FlagUtils.generate_fake_flag() for port in selected_flag_ports[1:]}

        # === Select random junk ports ===
        junk_response_pool = {
            "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
            "🔒 Unauthorized: API key required.",
            "503 Service Unavailable\nTry again later.",
            "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>",
            "DEBUG: Connection established successfully.",
            "💡 Tip: Scan only the ports you really need.",
            "ERROR 400: Bad request syntax.",
            "System maintenance in progress.",
            "Welcome to Experimental IoT Server (beta build).",
            "Python HTTP Server: directory listing not allowed.",
            "💻 Dev API v0.1 — POST requests only.",
            "403 Forbidden: You don’t have permission to access this resource.",
            "Error 418: I’m a teapot.",
            "Hello World!\nTest endpoint active.",
            "Server under maintenance.\nPlease retry later."
        }
        num_junk_ports = random.randint(8, 12)  # Pick 8–12 junk ports
        selected_junk_ports = self.random_ports(self.port_range, selected_flag_ports, num_junk_ports)
        junk_responses = {
            port: random.choice(list(junk_response_pool))
            for port in selected_junk_ports
        }

        # === Patch server.py with new data
        self.patch_server_file(real_flag, fake_flags, real_port, junk_responses)

        # === Return plaintext real flag
        print(f"🏁 Real flag: {real_flag} on port {real_port}")
        for port, flag in fake_flags.items():
            print(f"🎭 Fake flag: {flag} on port {port}")
        return real_flag
