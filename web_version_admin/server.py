try:
    # Flask 2.x: Markup is part of flask
    from flask import Flask, render_template, request, jsonify, Markup, send_from_directory
except ImportError:
    # Flask 3.x: Markup moved to markupsafe
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from markupsafe import Markup

import subprocess
import json
import os
import base64
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import markdown
import sys
sys.dont_write_bytecode = True  # 🛡 prevent .pyc files in admin

# === Base Directory ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === Add BASE_DIR to sys.path for imports ===
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# === Import backend logic ===
from ChallengeList import ChallengeList

# === Detect mode and select challenges.json path ===
server_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(server_dir) == "web_version_admin":
    mode = "admin"
    challenges_path = os.path.join(server_dir, "challenges.json")
else:
    mode = "student"
    challenges_path = os.path.join(server_dir, "challenges.json")

print(f"📖 Using challenges file at: {challenges_path}")

# === App Initialization ===
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "web_version", "templates"),
    static_folder=os.path.join(BASE_DIR, "web_version", "static")
)

DEBUG_MODE = os.environ.get("CCRI_DEBUG", "0") == "1"
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)

# === Load Challenges ===
try:
    print(f"Loading challenges from {challenges_path}...")
    challenges = ChallengeList(challenges_file=challenges_path)
    print(f"Loaded {challenges.numOfChallenges} challenges successfully.")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find '{challenges_path}'!")
    exit(1)
except json.JSONDecodeError:
    print(f"❌ ERROR: '{challenges_path}' contains invalid JSON!")
    exit(1)

# === Helper: XOR Decode ===
def xor_decode(encoded_base64, key):
    decoded_bytes = base64.b64decode(encoded_base64)
    return ''.join(
        chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(decoded_bytes)
    )

# === Routes ===
@app.route('/')
def index():
    return render_template('index.html', challenges=challenges)

@app.route('/challenge/<challenge_id>')
def challenge_view(challenge_id):
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return "Challenge not found", 404

    folder = selectedChallenge.getFolder()
    if not os.path.exists(folder):
        return f"⚠️ Challenge folder not found: {folder}", 404

    readme_html = ""
    readme_path = os.path.join(folder, 'README.txt')
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                raw_readme = f.read()
                readme_html = Markup(markdown.markdown(raw_readme))
        except Exception as e:
            readme_html = f"<p><strong>Error loading README:</strong> {e}</p>"

    file_list = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and f != "README.txt"
        and not f.startswith(".")
    ]

    return render_template('challenge.html', challenge=selectedChallenge, readme=readme_html, files=file_list)

@app.route('/challenge/<challenge_id>/file/<path:filename>')
def get_challenge_file(challenge_id, filename):
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return "Challenge not found", 404

    folder = selectedChallenge.getFolder()
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        return "File not found", 404

    return send_from_directory(folder, filename)

@app.route('/submit_flag/<challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    data = request.get_json()
    submitted_flag = data.get('flag', '').strip()
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)

    if selectedChallenge is None:
        print(f"❌ Challenge ID '{challenge_id}' not found.")
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    print(f"🌐 Running in {mode.upper()} mode")
    correct_flag = selectedChallenge.getFlag().strip()

    # === Debug: Print mode and flags
    print("====== FLAG DEBUG ======")
    print(f"🗂 Mode: {mode.upper()}")
    print(f"📥 Submitted flag: '{submitted_flag}'")
    print(f"🎯 Correct flag:   '{correct_flag}'")
    print("========================")

    if mode == "admin":
        if submitted_flag == correct_flag:
            print(f"✅ MATCH (Admin): Submitted flag matches correct flag.")
            selectedChallenge.setComplete()
            if selectedChallenge.getId() not in challenges.completed_challenges:
                challenges.completed_challenges.append(selectedChallenge.getId())
            return jsonify({"status": "correct"})
        else:
            print(f"❌ MISMATCH (Admin): Submitted flag does not match correct flag.")
            return jsonify({"status": "incorrect"}), 400
    else:
        try:
            decoded_flag = xor_decode(
                base64.b64decode(correct_flag),
                "CTF4EVER"
            ).strip()
            print(f"🎯 Decoded correct flag (Student): '{decoded_flag}'")
        except Exception as e:
            print(f"⚠️ Decode failed: {e}")
            return jsonify({"status": "error", "message": "Internal decoding error."}), 500

        if submitted_flag == decoded_flag:
            print(f"✅ MATCH (Student): Submitted flag matches decoded flag.")
            selectedChallenge.setComplete()
            if selectedChallenge.getId() not in challenges.completed_challenges:
                challenges.completed_challenges.append(selectedChallenge.getId())
            return jsonify({"status": "correct"})
        else:
            print(f"❌ MISMATCH (Student): Submitted flag does not match decoded flag.")
            return jsonify({"status": "incorrect"}), 400

@app.route('/open_folder/<challenge_id>', methods=['POST'])
def open_folder(challenge_id):
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    folder = selectedChallenge.getFolder()
    if not os.path.exists(folder):
        return jsonify({"status": "error", "message": "Challenge folder not found."}), 404

    try:
        subprocess.Popen(['xdg-open', folder], shell=False)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/run_script/<challenge_id>', methods=['POST'])
def run_script(challenge_id):
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    script_path = os.path.join(selectedChallenge.getFolder(), selectedChallenge.getScript())

    if not os.path.exists(script_path):
        return jsonify({"status": "error", "message": f"Script '{selectedChallenge.getScript()}' not found."}), 404

    try:
        if os.path.exists("/etc/parrot"):  # Parrot-specific marker file
            print("🐦 Detected Parrot OS. Forcing parrot-terminal.")
            subprocess.Popen([
                "parrot-terminal",
                "--working-directory", selectedChallenge.getFolder(),
                "-e", f"bash \"{script_path}\""
            ], shell=False)
            return jsonify({"status": "success"})

        fallback_terminals = ["gnome-terminal", "konsole", "xfce4-terminal", "lxterminal"]
        for term in fallback_terminals:
            if subprocess.call(["which", term], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                subprocess.Popen([
                    term,
                    "--working-directory", selectedChallenge.getFolder(),
                    "-e", f"bash \"{script_path}\""
                ], shell=False)
                return jsonify({"status": "success"})

        return jsonify({"status": "error", "message": "No supported terminal emulator found."}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# === Simulated Open Ports ===
FAKE_FLAGS = {
    8004: "NMAP-PORT-4312",
    8023: "SCAN-4312-PORT",
    8047: "CCRI-SCAN-8472",  # ✅ REAL FLAG
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

class PortHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = ALL_PORTS.get(self.server.server_port, "Connection refused")
        banner = f"👋 Welcome to {SERVICE_NAMES.get(self.server.server_port, 'http')} Service\n\n"
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Server", SERVICE_NAMES.get(self.server.server_port, "http"))
        self.end_headers()
        self.wfile.write((banner + response).encode("utf-8"))

    def log_message(self, format, *args):
        return  # Silence logs

def start_fake_service(port):
    try:
        server = HTTPServer(('0.0.0.0', port), PortHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"🛰️  Simulated service running on port {port} ({SERVICE_NAMES.get(port, 'http')})")
    except OSError as e:
        print(f"❌ Could not bind port {port}: {e}")

for port in FAKE_FLAGS:
    start_fake_service(port)

if __name__ == '__main__':
    print("🌐 Student hub running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
