try:
    # Flask 2.x: Markup is part of flask
    from flask import Flask, render_template, request, jsonify, send_from_directory, Markup
except ImportError:
    # Flask 3.x: Markup moved to markupsafe
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from markupsafe import Markup

import subprocess
import json
import os
import base64
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import markdown

# === Helper: Find Project Root ===
def find_project_root(marker=".ccri_ctf_root"):
    """Walk upwards to locate the project root by marker file."""
    dir_path = os.path.abspath(os.path.dirname(__file__))
    while dir_path != "/":
        if os.path.isfile(os.path.join(dir_path, marker)):
            return dir_path
        dir_path = os.path.dirname(dir_path)
    raise RuntimeError(f"❌ Could not find project root marker '{marker}'. Are you inside the CTF repo?")

# === Resolve BASE DIRECTORIES ===
PROJECT_ROOT = find_project_root()
WEB_ADMIN_DIR = os.path.join(PROJECT_ROOT, "web_version_admin")
CHALLENGES_DIR = os.path.join(PROJECT_ROOT, "challenges")

CHALLENGES_JSON_PATH = os.path.join(WEB_ADMIN_DIR, "challenges.json")
TEMPLATES_DIR = os.path.join(WEB_ADMIN_DIR, "templates")
STATIC_DIR = os.path.join(WEB_ADMIN_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# === Hardcoded XOR Key ===
XOR_KEY = "CTF4EVER"

# === Load student challenges.json ===
try:
    with open(CHALLENGES_JSON_PATH, 'r', encoding='utf-8') as f:
        raw_challenges = json.load(f)
except FileNotFoundError:
    print(f"❌ ERROR: Could not find 'challenges.json' at {CHALLENGES_JSON_PATH}")
    exit(1)
except json.JSONDecodeError:
    print(f"❌ ERROR: 'challenges.json' contains invalid JSON!")
    exit(1)

# Normalize challenge folder paths relative to WEB_ADMIN_DIR
challenges = {}
for cid, meta in raw_challenges.items():
    abs_folder_path = os.path.normpath(os.path.join(WEB_ADMIN_DIR, meta["folder"]))
    meta["folder"] = abs_folder_path
    challenges[cid] = meta

# === Helper: XOR Decode ===
def xor_decode(encoded_base64, key):
    decoded_bytes = base64.b64decode(encoded_base64)
    return ''.join(
        chr(b ^ ord(key[i % len(key)]))
        for i, b in enumerate(decoded_bytes)
    )

# === Flask Routes ===
@app.route('/')
def index():
    """Main grid of all challenges"""
    return render_template('index.html', challenges=challenges)

@app.route('/challenge/<challenge_id>')
def challenge_view(challenge_id):
    """View a specific challenge"""
    if challenge_id not in challenges:
        return "Challenge not found", 404

    challenge = challenges[challenge_id]
    folder = challenge['folder']

    # Read README.txt if it exists
    readme_path = os.path.join(folder, 'README.txt')
    readme_html = ""
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                raw_readme = f.read()
                readme_html = Markup(markdown.markdown(raw_readme))
        except Exception as e:
            readme_html = f"<p><strong>Error loading README:</strong> {e}</p>"

    # List other files (excluding README and hidden files)
    file_list = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and f != "README.txt"
        and not f.startswith(".")
    ]

    return render_template(
        'challenge.html',
        challenge_id=challenge_id,
        challenge=challenge,
        readme=readme_html,
        files=file_list
    )

@app.route('/challenge_file/<challenge_id>/<path:filename>')
def get_challenge_file(challenge_id, filename):
    """Serve files from the challenge folder."""
    if challenge_id not in challenges:
        return "Challenge not found", 404

    folder = challenges[challenge_id]['folder']
    return send_from_directory(folder, filename)

@app.route('/submit_flag/<challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    """Validate submitted flag"""
    data = request.get_json()
    submitted_flag = data.get('flag', '').strip().upper()

    if challenge_id not in challenges:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    correct_flag = xor_decode(challenges[challenge_id]['flag'], XOR_KEY).upper()

    if submitted_flag == correct_flag:
        return jsonify({"status": "correct"})
    else:
        return jsonify({"status": "incorrect"})

@app.route('/open_folder/<challenge_id>', methods=['POST'])
def open_folder(challenge_id):
    """Open the challenge folder in the file manager"""
    if challenge_id not in challenges:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    folder = challenges[challenge_id]['folder']
    try:
        # Try xdg-open first, fallback to gio open
        try:
            subprocess.Popen(['xdg-open', folder])
        except FileNotFoundError:
            subprocess.Popen(['gio', 'open', folder])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/run_script/<challenge_id>', methods=['POST'])
def run_script(challenge_id):
    """Launch the helper script for this challenge in a terminal."""
    if challenge_id not in challenges:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    folder = challenges[challenge_id]['folder']
    script_name = challenges[challenge_id]['script']
    script_path = os.path.join(folder, script_name)

    if not os.path.isfile(script_path):
        return jsonify({"status": "error", "message": f"Script '{script_name}' not found."}), 404

    try:
        # Prefer x-terminal-emulator, fallback to common terminals
        terminals = ["x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "lxterminal"]
        for term in terminals:
            if subprocess.call(["which", term], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                subprocess.Popen([term, "--working-directory", folder, "-e", f"bash \"{script_path}\""])
                return jsonify({"status": "success"})

        # No terminal found
        return jsonify({"status": "error", "message": "No terminal emulator found on this system."}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# === Simulated Open Ports (Challenge #17) ===
FAKE_FLAGS = {
    8004: "NMAP-PORT-4312",
    8023: "SCAN-4312-PORT",
    8047: "CCRI-SCAN-8472",       # ✅ REAL FLAG
    8072: "OPEN-SERVICE-9281",
    8095: "HTTP-7721-SERVER"
}

SERVICE_NAMES = {
    8004: "configd",
    8023: "metricsd",
    8047: "sysmon-api",
    8072: "update-agent",
    8095: "metrics-gateway"
}

ALL_PORTS = FAKE_FLAGS.copy()

class PortHandler(BaseHTTPRequestHandler):
    """Custom HTTP handler for simulated ports"""
    def do_GET(self):
        response = ALL_PORTS.get(self.server.server_port, "Connection refused")
        service_name = SERVICE_NAMES.get(self.server.server_port, "http")
        banner = f"👋 Welcome to {service_name} Service\n\n"
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Server", service_name)
        self.end_headers()
        self.wfile.write((banner + response).encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress logging
        return

def start_fake_service(port):
    """Start a lightweight HTTP server on the given port"""
    try:
        server = HTTPServer(('0.0.0.0', port), PortHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"🛰️  Simulated service running on port {port} ({SERVICE_NAMES.get(port, 'http')})")
    except OSError as e:
        print(f"❌ Could not bind port {port}: {e}")

# Start all fake services
for port in ALL_PORTS:
    start_fake_service(port)

# === Start Flask Hub ===
if __name__ == '__main__':
    print("🌐 Student hub running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)
