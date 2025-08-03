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
    flags, service names, and junk responses. Stores unlock metadata in memory.
    """

    def __init__(self, project_root: Path = None, server_file: Path = None, mode="guided"):
        self.project_root = project_root or self.find_project_root()
        self.server_file = server_file or self.project_root / "web_version_admin" / "server.py"
        self.mode = mode
        self.port_range = list(range(8000, 8100)) if self.mode == "guided" else list(range(9000, 9100))
        self.metadata = {}

    @staticmethod
    def find_project_root() -> Path:
        dir_path = Path.cwd()
        for parent in [dir_path] + list(dir_path.parents):
            if (parent / ".ccri_ctf_root").exists():
                return parent.resolve()
        print("❌ ERROR: Could not find .ccri_ctf_root marker.", file=sys.stderr)
        sys.exit(1)

    def random_ports(self, port_range, exclude_ports, count):
        available = set(port_range) - set(exclude_ports)
        return random.sample(sorted(available), count)

    def escape_python_string_literal(self, s: str) -> str:
        return '"' + s.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"') + '"'

    def patch_server_file(self, real_flag: str, fake_flags: dict, real_port: int, junk_ports: dict):
        server_file = self.server_file.resolve()

        if not server_file.exists():
            print(f"❌ ERROR: {server_file} not found.", file=sys.stderr)
            sys.exit(1)

        try:
            flag_var = "GUIDED_FAKE_FLAGS" if self.mode == "guided" else "SOLO_FAKE_FLAGS"
            junk_var = "GUIDED_JUNK_RESPONSES" if self.mode == "guided" else "SOLO_JUNK_RESPONSES"
            service_var = "GUIDED_SERVICE_NAMES" if self.mode == "guided" else "SOLO_SERVICE_NAMES"

            all_ports = [real_port] + list(fake_flags.keys()) + list(junk_ports.keys())
            service_name_pool = [
                "alpha-core", "delta-sync", "gamma-relay", "beta-hub", "lambda-api", "omega-stream",
                "theta-daemon", "epsilon-sync", "kappa-node", "zeta-cache", "delta-proxy",
                "sysmon-api", "configd", "metricsd", "auth-service", "update-agent"
            ]
            random.shuffle(service_name_pool)
            combined_service_names = {
                port: service_name_pool[i % len(service_name_pool)]
                for i, port in enumerate(all_ports)
            }

            new_fake_flags = [f"    {real_port}: \"{real_flag}\",       # ✅ REAL FLAG"]
            for port, flag in fake_flags.items():
                new_fake_flags.append(f"    {port}: \"{flag}\",       # fake")
            new_fake_flags_block = f"{flag_var} = {{\n" + "\n".join(new_fake_flags) + "\n}"

            new_junk_responses = []
            for port in sorted(junk_ports):
                safe_response = self.escape_python_string_literal(junk_ports[port])
                new_junk_responses.append(f"    {port}: {safe_response}")
            new_junk_block = f"{junk_var} = {{\n" + ",\n".join(new_junk_responses) + "\n}"

            service_name_updates = [
                f"    {port}: \"{combined_service_names[port]}\"" for port in sorted(combined_service_names)
            ]
            new_service_names_block = f"{service_var}.update({{\n" + ",\n".join(service_name_updates) + "\n}})"
            base_service_block = f"{service_var} = {{\n" + ",\n".join(service_name_updates) + "\n}"

            print(f"📂 Reading {server_file}...")
            content = server_file.read_text(encoding="utf-8")

            new_content, count_flags = re.subn(
                rf"{flag_var}\s*=\s*\{{[^}}]*\}}",
                new_fake_flags_block,
                content,
                flags=re.DOTALL
            )
            if count_flags == 0:
                raise RuntimeError(f"No {flag_var} block found to replace!")

            new_content, count_junk = re.subn(
                rf"{junk_var}\s*=\s*\{{[^}}]*\}}",
                new_junk_block,
                new_content,
                flags=re.DOTALL
            )
            if count_junk == 0:
                raise RuntimeError(f"No {junk_var} block found to replace!")

            new_content, count_base_services = re.subn(
                rf"{service_var}\s*=\s*\{{[^}}]*\}}",
                base_service_block,
                new_content,
                flags=re.DOTALL
            )
            if count_base_services == 0:
                print(f"⚠️ WARNING: No base assignment for {service_var} found — skipping.")

            new_content, count_update_block = re.subn(
                rf"{service_var}\.update\(\s*\{{[^}}]*\}}\s*\)",
                new_service_names_block,
                new_content,
                flags=re.DOTALL
            )
            if count_update_block == 0:
                new_content = new_content.replace(
                    "# Combine real flags and junk responses",
                    "# Combine real flags and junk responses\n" + new_service_names_block
                )

            backup_file = server_file.with_suffix(".bak")
            if not backup_file.exists():
                server_file.replace(backup_file)
                print(f"🗄️ Backup created: {backup_file.name}")
            else:
                print(f"🗄️ Backup already exists: {backup_file.name}")

            server_file.write_text(new_content, encoding="utf-8")
            print(f"✅ Updated {server_file.name} with {flag_var}, {junk_var}, and {service_var} data.")

            self.metadata = {
                "real_flag": real_flag,
                "real_port": real_port,
                "server_file": str(server_file.relative_to(self.project_root)),
                "unlock_method": f"Scan ports {self.port_range[0]}–{self.port_range[-1]} and query HTTP endpoints to locate the real flag (port {real_port})",
                "hint": f"Use nmap -p{self.port_range[0]}-{self.port_range[-1]} localhost to discover ports and curl to check flags."
            }

        except Exception as e:
            print(f"❌ ERROR during server.py patching: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_flag(self, challenge_folder: Path) -> str:
        selected_flag_ports = self.random_ports(self.port_range, [], 5)
        real_port = selected_flag_ports[0]
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = {port: FlagUtils.generate_fake_flag() for port in selected_flag_ports[1:]}

        junk_response_pool = [
            "Welcome to Dev HTTP Server v1.3\\nPlease login to continue.",
            "🔒 Unauthorized: API key required.",
            "503 Service Unavailable\\nTry again later.",
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
            "Hello World!\\nTest endpoint active.",
            "Server under maintenance.\\nPlease retry later."
        ]
        selected_junk_ports = self.random_ports(self.port_range, selected_flag_ports, random.randint(8, 12))
        junk_responses = {port: random.choice(junk_response_pool) for port in selected_junk_ports}

        self.patch_server_file(real_flag, fake_flags, real_port, junk_responses)

        print(f"🏁 Real flag: {real_flag} on port {real_port}")
        for port, flag in fake_flags.items():
            print(f"🎭 Fake flag: {flag} on port {port}")

        # Save unlock metadata just like other generators
        unlocks_file = self.project_root / "web_version_admin" / (
            "validation_unlocks.json" if self.mode == "guided" else "validation_unlocks_solo.json"
        )
        challenge_id = "17_Nmap_Scanning"
        existing = {}
        if unlocks_file.exists():
            with open(unlocks_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing[challenge_id] = self.metadata
        with open(unlocks_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)
        print(f"📦 Saved unlock data to {unlocks_file.name}")

        return real_flag, self.metadata
