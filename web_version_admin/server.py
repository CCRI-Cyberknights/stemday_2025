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
    template_folder = os.path.join(server_dir, "templates")
    static_folder = os.path.join(server_dir, "static")
else:
    mode = "student"
    challenges_path = os.path.join(server_dir, "challenges.json")
    template_folder = os.path.join(server_dir, "templates")
    static_folder = os.path.join(server_dir, "static")

print(f"📖 Using challenges file at: {challenges_path}")
print(f"📖 Using template folder at: {template_folder}")

# === App Initialization ===
app = Flask(
    __name__,
    template_folder=template_folder,
    static_folder=static_folder
)

DEBUG_MODE = os.environ.get("CCRI_DEBUG", "0") == "1"
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)
print(f"DEBUG: server_dir = {server_dir}")
print(f"DEBUG: mode = {mode}")
print(f"DEBUG: Rendering with mode={mode}")

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

# === Flask Routes ===
@app.route('/')
def index():
    return render_template('index.html', challenges=challenges, mode=mode)

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
            decoded_flag = xor_decode(correct_flag, "CTF4EVER").strip()
            print(f"🎯 Decoded correct flag (Student): '{decoded_flag}'")
        except Exception as e:
            print(f"⚠️ Decode failed in student mode: {e}")
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
        if os.path.exists("/etc/parrot"):
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

# === Simulated Open Ports (Realistic Nmap Network) ===
FAKE_FLAGS = {
    8004: "NMAP-PORT-4312",
    8023: "SCAN-4312-PORT",
    8047: "CCRI-SCAN-8472",  # ✅ REAL FLAG
    8072: "OPEN-SERVICE-9281",
    8095: "HTTP-7721-SERVER"
}

JUNK_RESPONSES = {
    8001: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    8009: "🔒 Unauthorized: API key required.",
    8015: "503 Service Unavailable\nTry again later.",
    8020: "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>",
    8028: "DEBUG: Connection established successfully.",
    8033: "💡 Tip: Scan only the ports you really need.",
    8039: "ERROR 400: Bad request syntax.",
    8045: "System maintenance in progress. Expected downtime: 13 minutes.",
    8051: "Welcome to Experimental IoT Server (beta build).",
    8058: "Python HTTP Server: directory listing not allowed.",
    8064: "💻 Dev API v0.1 — POST requests only.",
    8077: "403 Forbidden: You don’t have permission to access this resource.",
    8083: "Error 418: I’m a teapot.",
    8089: "Hello World!\nTest endpoint active.",
    8098: "Server under maintenance.\nPlease retry in 5 minutes."
}

SERVICE_NAMES = {
    8001: "dev-http",
    8004: "flag-api",
    8009: "secure-api",
    8015: "maintenance",
    8020: "apache",
    8023: "flag-api",
    8028: "debug-service",
    8033: "help-service",
    8039: "http",
    8045: "maintenance",
    8047: "flag-api",
    8051: "iot-server",
    8058: "http",
    8064: "dev-api",
    8072: "flag-api",
    8077: "secure-api",
    8083: "http",
    8089: "test-service",
    8095: "flag-api",
    8098: "maintenance"
}

SERVICE_NAMES.update({
    # Example: generator will overwrite these dynamically
})

ALL_PORTS = {**JUNK_RESPONSES, **FAKE_FLAGS}

class PortHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = ALL_PORTS.get(self.server.server_port, "Connection refused")
        service_name = SERVICE_NAMES.get(self.server.server_port, "http")
        banner = f"👋 Welcome to {service_name} Service\n\n"
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Server", service_name)
        self.send_header("X-Service-Name", service_name)
        self.end_headers()
        self.wfile.write((banner + response).encode("utf-8"))

    def log_message(self, format, *args):
        return

def start_fake_service(port):
    try:
        server = HTTPServer(('0.0.0.0', port), PortHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"🛰️  Simulated service running on port {port} ({SERVICE_NAMES.get(port, 'http')})")
    except OSError as e:
        print(f"❌ Could not bind port {port}: {e}")

for port in range(8000, 8101):
    start_fake_service(port)

if __name__ == '__main__':
    print(f"🌐 {mode.capitalize()} hub running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
