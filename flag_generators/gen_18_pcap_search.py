#!/usr/bin/env python3

try:
    from scapy.all import IP, TCP, Raw, wrpcap
except ImportError:
    print("❌ Scapy is not installed. Run: sudo apt install python3-scapy")
    exit(1)

import random
import sys
from pathlib import Path
from flag_generators.flag_helpers import FlagUtils


class PcapSearchFlagGenerator:
    """
    Generator for the PCAP Search challenge.
    Creates a traffic.pcap file with embedded real and fake flags.
    Stores unlock metadata for validation workflow.
    """

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or self.find_project_root()
        self.metadata = {}  # For unlock info

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

    def http_packet(self, src, dst, sport, dport, payload):
        """
        Craft a TCP packet with HTTP payload.
        """
        ip = IP(src=src, dst=dst)
        tcp = TCP(sport=sport, dport=dport, flags="PA", seq=random.randint(1000, 5000))
        raw = Raw(load=payload)
        return ip / tcp / raw

    def http_conversation(self, src, dst, flag=None, noise=False, real_flag=False):
        """
        Build a realistic HTTP conversation.
        """
        sport = random.randint(1024, 65535)
        dport = 80
        packets = []

        # Client sends HTTP GET
        packets.append(self.http_packet(
            src, dst, sport, dport,
            f"GET / HTTP/1.1\r\nHost: {dst}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n".encode()
        ))

        # Server responds
        server_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Server: nginx/1.18.0\r\n"
            "Content-Type: text/html\r\n"
            "Set-Cookie: sessionid=" +
            ''.join(random.choices('abcdef1234567890', k=10)) + "; HttpOnly\r\n"
        )

        # Embed flag in header if real
        if real_flag:
            server_headers += f"X-Flag: {flag}\r\n"

        # Body content
        if noise:
            body = "<html><body><p>Welcome to our web server.</p></body></html>"
        elif flag and not real_flag:
            # Fake flags as distractions in HTML comments
            body = f"<html><body><!-- DEBUG: Found flag {flag} --></body></html>"
        else:
            body = "<html><body><p>Hello, authorized user.</p></body></html>"

        response = f"{server_headers}\r\n{body}".encode()
        packets.append(self.http_packet(dst, src, dport, sport, response))
        return packets

    def embed_pcap(self, challenge_folder: Path, real_flag: str, fake_flags: list):
        """
        Generate traffic.pcap file with noise, fake flags, and one real flag.
        """
        challenge_folder.mkdir(parents=True, exist_ok=True)

        # Remove old traffic.pcap if it exists
        output_file = challenge_folder / "traffic.pcap"
        if output_file.exists():
            try:
                output_file.unlink()
                print(f"🗑️ Removed old file: {output_file.relative_to(self.project_root)}")
            except Exception as e:
                print(f"⚠️ Could not delete old traffic.pcap: {e}", file=sys.stderr)

        packets = []

        # Random noise traffic (~150 conversations)
        for _ in range(150):
            src = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            dst = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            packets.extend(self.http_conversation(src, dst, noise=True))

        # Embed fake flags
        for fake in fake_flags:
            src = f"172.16.{random.randint(0,255)}.{random.randint(1,254)}"
            dst = f"172.16.{random.randint(0,255)}.{random.randint(1,254)}"
            packets.extend(self.http_conversation(src, dst, flag=fake))

        # Embed the real flag (header only, no hint in body)
        src = "192.168.50.10"
        dst = "192.168.50.20"
        packets.extend(self.http_conversation(src, dst, flag=real_flag, real_flag=True))

        # Shuffle packets for realism
        random.shuffle(packets)

        # Write PCAP (overwrite safely)
        wrpcap(str(output_file), packets)

        print(f"✅ traffic.pcap created: {output_file.relative_to(self.project_root)}")
        print(f"   🏁 Real flag: {real_flag}")
        print(f"   🎭 Fake flags: {', '.join(fake_flags)}")
        print(f"📦 Total packets: {len(packets)}")

        # Record unlock metadata
        self.metadata = {
            "real_flag": real_flag,
            "challenge_file": str(output_file.relative_to(self.project_root)),
            "unlock_method": "Analyze traffic.pcap for flags in HTTP headers using Wireshark or tshark",
            "hint": "Filter for HTTP headers in Wireshark (e.g., http.header) or grep for 'X-Flag:'"
        }

    def generate_flag(self, challenge_folder: Path) -> str:
        """
        Generate traffic.pcap with 1 real and 4 fake flags.
        Return the real flag for challenges.json.
        """
        real_flag = FlagUtils.generate_real_flag()
        fake_flags = []
        while len(fake_flags) < 4:
            fake = FlagUtils.generate_fake_flag()
            if fake != real_flag and fake not in fake_flags:
                fake_flags.append(fake)

        self.embed_pcap(challenge_folder, real_flag, fake_flags)
        return real_flag
