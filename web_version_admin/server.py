try:
    # Flask 2.x: Markup is part of flask
    from flask import Flask, render_template, request, jsonify, Markup
except ImportError:
    # Flask 3.x: Markup moved to markupsafe
    from flask import Flask, render_template, request, jsonify
    from markupsafe import Markup

import subprocess
import json
import os
import base64
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from ChallengeList import ChallengeList

# New import for Markdown support
import markdown

app = Flask(__name__)

# === Hardcoded XOR Key ===
XOR_KEY = "CTF4EVER"

# === Load student challenges.json ===
try:
    print("Loading challenges from challenges.json...")
    challenges = ChallengeList()
    print(f"Loaded {challenges.numOfChallenges} challenges successfully.")
except FileNotFoundError:
    print("❌ ERROR: Could not find 'challenges.json' in the current directory!")
    exit(1)
except json.JSONDecodeError:
    print("❌ ERROR: 'challenges.json' contains invalid JSON!")
    exit(1)

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
    """Returns challenge overview page"""
    return render_template('index.html', challenges=challenges)

@app.route('/challenge/<challenge_id>')
def challenge_view(challenge_id):
    """Returns challenge details page"""

    # === Validate challenge_id ===
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return "Challenge not found", 404

    # Store challenge and folder info
    folder = selectedChallenge.getFolder()

    # Read README.txt if it exists
    readme_path = os.path.join(folder, 'README.txt')
    readme_html = ""
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                raw_readme = f.read()
                # Convert Markdown to HTML
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
        challenge=selectedChallenge,
        readme=readme_html,
        files=file_list
    )

@app.route('/submit_flag/<challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    """Validate submitted flag"""
    # Store user provided flag
    data = request.get_json()
    submitted_flag = data.get('flag', '').strip().upper()
    
    # Get challenge by ID
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    # Get the correct flag for the challenge
    correct_flag = selectedChallenge.getFlag().strip().upper()

    if submitted_flag == correct_flag:
        # Mark challenge as completed
        for challenge in challenges.challenges:
            if challenge.getId() == selectedChallenge.getId():
                challenge.setComplete()
                print(f"Challenge {selectedChallenge.getName()} completed by user.")
                break
        # Add challenge to completed challenges list
        if selectedChallenge.getId() not in challenges.completed_challenges:
            print(f"Adding challenge {selectedChallenge.getName()} to completed challenges.")
            challenges.completed_challenges.append(selectedChallenge.getId())
        # Return success response
        return jsonify({"status": "correct"})
    else:
        # Return incorrect response
        print(f"Incorrect flag submitted for challenge {selectedChallenge.getName()}.")
        return jsonify({"status": "incorrect"})

@app.route('/open_folder/<challenge_id>', methods=['POST'])
def open_folder(challenge_id):
    """Open the challenge folder in the file manager"""
    # === Validate challenge_id ===
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    folder = selectedChallenge.getFolder()
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
    # === Validate challenge_id ===
    selectedChallenge = challenges.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    folder = selectedChallenge.getFolder()
    script_name = selectedChallenge.getScript()
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
