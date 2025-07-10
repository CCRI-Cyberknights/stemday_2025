#!/usr/bin/env python3
from scapy.all import *
import random
import os

# === Constants ===
REAL_FLAG = "CCRI-NETW-7315"
FAKE_FLAGS = [
    "FLAG-FAKE-1111",
    "NETW-5555-FAKE",
    "CCRI-2222-WRNG",
    "FAKE-3333-DATA",
]

# === Utility: Generate HTTP packets ===
def http_packet(src, dst, sport, dport, payload):
    ip = IP(src=src, dst=dst)
    tcp = TCP(sport=sport, dport=dport, flags="PA", seq=random.randint(1000,5000))
    raw = Raw(load=payload)
    return ip / tcp / raw

# === Build a realistic HTTP conversation ===
def http_conversation(src, dst, flag=None, noise=False, real_flag=False):
    sport = random.randint(1024, 65535)
    dport = 80
    packets = []

    # Client sends HTTP GET
    packets.append(http_packet(src, dst, sport, dport,
        f"GET / HTTP/1.1\r\nHost: {dst}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n".encode()))

    # Server responds
    server_headers = (
        "HTTP/1.1 200 OK\r\n"
        "Server: nginx/1.18.0\r\n"
        "Content-Type: text/html\r\n"
        "Set-Cookie: sessionid=" + ''.join(random.choices('abcdef1234567890', k=10)) + "; HttpOnly\r\n"
    )

    # Embed flag in header if it's the real flag
    if real_flag:
        server_headers += f"X-Flag: {flag}\r\n"

    # Create body content
    if noise:
        body = "<html><body><p>Welcome to our web server.</p></body></html>"
    elif flag and not real_flag:
        # Fake flags appear in the HTML body as distractions
        body = f"<html><body><!-- DEBUG: Found flag {flag} --></body></html>"
    else:
        body = "<html><body><p>Hello, authorized user.</p></body></html>"

    response = f"{server_headers}\r\n{body}".encode()

    packets.append(http_packet(dst, src, dport, sport, response))
    return packets

# === Generate Traffic ===
packets = []

# Generate random noise: ~150 conversations
for _ in range(150):
    src = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    dst = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    packets.extend(http_conversation(src, dst, noise=True))

# Embed 4 fake flags (each with verbose conversations)
for fake in FAKE_FLAGS:
    src = f"172.16.{random.randint(0,255)}.{random.randint(1,254)}"
    dst = f"172.16.{random.randint(0,255)}.{random.randint(1,254)}"
    packets.extend(http_conversation(src, dst, flag=fake))

# Embed the real flag (header only, no hint in body)
src = "192.168.50.10"
dst = "192.168.50.20"
packets.extend(http_conversation(src, dst, flag=REAL_FLAG, real_flag=True))

# Shuffle packets for realism
random.shuffle(packets)

# === Write PCAP to same directory as script ===
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, "traffic.pcap")

wrpcap(output_file, packets)

print(f"✅ Fake traffic written to {output_file}")
print(f"💡 Embedded flags: 1 real (header only: {REAL_FLAG}), {len(FAKE_FLAGS)} fakes (HTML bodies)")
print(f"📦 Total packets: {len(packets)}")
