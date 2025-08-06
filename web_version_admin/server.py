try:
    # Flask 2.x: Markup is part of flask
    from flask import Flask, render_template, request, jsonify, Markup, send_from_directory, redirect, url_for, session
except ImportError:
    # Flask 3.x: Markup moved to markupsafe
    from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
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

sys.dont_write_bytecode = True  # 🔡 prevent .pyc files in admin

# === Base Directory ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# === Add BASE_DIR to sys.path for imports ===
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# === Import backend logic ===
from ChallengeList import ChallengeList

# === Flask App Initialization ===
server_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(server_dir, "templates")
static_folder = os.path.join(server_dir, "static")

app = Flask(
    __name__,
    template_folder=template_folder,
    static_folder=static_folder
)

app.secret_key = "super_secret_key"  # required for session tracking
DEBUG_MODE = os.environ.get("CCRI_DEBUG", "0") == "1"
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)

# === Detect Admin or Student Mode (ENV-first, then folder name) ===
base_mode = os.environ.get("CCRI_CTF_MODE", "").strip().lower()

if not base_mode:
    if os.path.basename(server_dir) == "web_version_admin":
        base_mode = "admin"
    else:
        base_mode = "student"

print(f"📖 Using template folder at: {template_folder}")
print(f"DEBUG: Base mode = {base_mode}")

# === Simulated Open Ports (dictionaries will be overwritten by generator) ===
GUIDED_FAKE_FLAGS = {
    8025: "CCRI-CAUF-7042",       # ✅ REAL FLAG
    8045: "STCZ-FMIN-8138",       # fake
    8003: "SEZI-7973-KYCG",       # fake
    8088: "OXDH-RCLZ-7945",       # fake
    8002: "UDCC-2879-PUUE",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8008: "💡 Tip: Scan only the ports you really need.",
    8028: "Python HTTP Server: directory listing not allowed.",
    8047: "DEBUG: Connection established successfully.",
    8048: "💡 Tip: Scan only the ports you really need.",
    8049: "ERROR 400: Bad request syntax.",
    8061: "💻 Dev API v0.1 — POST requests only.",
    8089: "💡 Tip: Scan only the ports you really need.",
    8099: "ERROR 400: Bad request syntax."
}
GUIDED_SERVICE_NAMES = {
    8002: "beta-hub",
    8003: "kappa-node",
    8008: "update-agent",
    8025: "sysmon-api",
    8028: "auth-service",
    8045: "theta-daemon",
    8047: "delta-proxy",
    8048: "alpha-core",
    8049: "lambda-api",
    8061: "metricsd",
    8088: "omega-stream",
    8089: "delta-sync",
    8099: "zeta-cache"
}
SOLO_FAKE_FLAGS = {
    9029: "CCRI-RVSU-2416",       # ✅ REAL FLAG
    9011: "IKDX-AVHQ-8310",       # fake
    9053: "GAJL-6131-NBBK",       # fake
    9054: "TVRL-ZYCR-7790",       # fake
    9047: "CFDY-UPGR-2840",       # fake
}
SOLO_JUNK_RESPONSES = {
    9003: "Python HTTP Server: directory listing not allowed.",
    9022: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    9032: "403 Forbidden: You don’t have permission to access this resource.",
    9035: "System maintenance in progress.",
    9046: "Error 418: I’m a teapot.",
    9051: "503 Service Unavailable\nTry again later.",
    9077: "🔒 Unauthorized: API key required.",
    9078: "System maintenance in progress.",
    9084: "403 Forbidden: You don’t have permission to access this resource."
}
SOLO_SERVICE_NAMES = {
    9003: "sysmon-api",
    9011: "epsilon-sync",
    9022: "update-agent",
    9029: "configd",
    9032: "theta-daemon",
    9035: "alpha-core",
    9046: "gamma-relay",
    9047: "kappa-node",
    9051: "zeta-cache",
    9053: "delta-sync",
    9054: "auth-service",
    9077: "omega-stream",
    9078: "beta-hub",
    9084: "lambda-api"
}

GUIDED_ALL_PORTS = {**GUIDED_JUNK_RESPONSES, **GUIDED_FAKE_FLAGS}
SOLO_ALL_PORTS = {**SOLO_JUNK_RESPONSES, **SOLO_FAKE_FLAGS}

# === Dynamic HTTP Handler Factory ===
def PortHandlerFactory(response_map, service_map):
    class CustomPortHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            response = response_map.get(self.server.server_port, "Connection refused")
            service_name = service_map.get(self.server.server_port, "http")
            banner = f"👋 Welcome to {service_name} Service\n\n"
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.send_header("Server", service_name)
            self.send_header("X-Service-Name", service_name)
            self.end_headers()
            self.wfile.write((banner + response).encode("utf-8"))

        def log_message(self, format, *args):
            return
    return CustomPortHandler

# === Start Simulated Services ===
def start_fake_service(port, response_map, service_map):
    try:
        server = HTTPServer(('0.0.0.0', port), PortHandlerFactory(response_map, service_map))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"🚁️  Simulated service running on port {port} ({service_map.get(port, 'http')})")
    except OSError as e:
        print(f"❌ Could not bind port {port}: {e}")

# Start Guided Mode Services (8000–8100)
for port in GUIDED_ALL_PORTS.keys():
    start_fake_service(port, GUIDED_ALL_PORTS, GUIDED_SERVICE_NAMES)

# Start Solo Mode Services (9000–9100)
for port in SOLO_ALL_PORTS.keys():
    start_fake_service(port, SOLO_ALL_PORTS, SOLO_SERVICE_NAMES)

# === Helper: Load Challenges ===
def load_challenges(mode="regular"):
    if mode == "solo":
        challenges_path = os.path.join(server_dir, "challenges_solo.json")
        challenges_folder = "challenges_solo"
    else:
        challenges_path = os.path.join(server_dir, "challenges.json")
        challenges_folder = "challenges"

    print(f"📖 Loading {mode.upper()} challenges from {challenges_path}")

    try:
        challenge_list = ChallengeList(challenges_file=challenges_path)
        list_type = "Guided" if mode == "regular" else "Solo"
        user_type = "Admin" if base_mode == "admin" else "Student"
        print(f"✅ {user_type} {list_type} Challenge List loaded ({challenge_list.numOfChallenges} challenges).")
        return challenge_list, challenges_folder
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find '{challenges_path}'!")
        exit(1)
    except json.JSONDecodeError:
        print(f"❌ ERROR: '{challenges_path}' contains invalid JSON!")
        exit(1)

# === Flask Routes ===
@app.route('/')
def landing_page():
    print(f"🌐 {base_mode.capitalize()} Hub loaded at http://127.0.0.1:5000")
    return render_template('landing.html', base_mode=base_mode)

@app.route('/set_mode/<mode>')
def set_mode(mode):
    if mode not in ["regular", "solo"]:
        return "Invalid mode", 400
    session["mode"] = mode
    print(f"🌐 Mode set to: {mode.upper()}")
    return redirect(url_for('index'))

@app.route('/challenges')
def index():
    mode = session.get("mode", "regular")
    challenge_list, challenges_folder = load_challenges(mode)

    if base_mode == "admin":
        list_title = f"Admin {'Guided' if mode == 'regular' else 'Solo'} Challenge List"
    else:
        list_title = f"Student {'Guided' if mode == 'regular' else 'Solo'} Challenge List"

    print(f"📄 Opening {list_title}...")
    return render_template('index.html', 
                           challenges=challenge_list, 
                           base_mode=base_mode, 
                           mode=mode, 
                           list_title=list_title)

@app.route('/challenge/<challenge_id>')
def challenge_view(challenge_id):
    mode = session.get("mode", "regular")
    challenge_list, challenges_folder = load_challenges(mode)

    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
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

    template = "challenge_solo.html" if mode == "solo" else "challenge.html"
    print(f"➡️ Opening {selectedChallenge.getName()} in {mode.upper()} mode.")
    return render_template(template, 
                           challenge=selectedChallenge, 
                           readme=readme_html, 
                           files=file_list, 
                           base_mode=base_mode, 
                           mode=mode)

@app.route('/submit_flag/<challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    mode = session.get("mode", "regular")
    challenge_list, _ = load_challenges(mode)
    selected_challenge = challenge_list.get_challenge_by_id(challenge_id)

    if selected_challenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    data = request.get_json()
    submitted_flag = data.get("flag", "").strip()
    real_flag = selected_challenge.getFlag().strip()

    if submitted_flag == real_flag:
        print(f"✅ Correct flag submitted for {challenge_id}")
        return jsonify({"status": "correct"})
    else:
        print(f"❌ Incorrect flag submitted for {challenge_id}")
        return jsonify({"status": "incorrect"})



@app.route('/open_folder/<challenge_id>', methods=['POST'])
def open_folder(challenge_id):
    challenge_list, _ = load_challenges(session.get("mode", "regular"))
    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    folder_path = selectedChallenge.getFolder()
    print(f"📂 Opening folder: {folder_path}")
    try:
        if sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', folder_path])
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', folder_path])
        elif sys.platform.startswith('win'):
            subprocess.Popen(['explorer', folder_path])
        else:
            return jsonify({"status": "error", "message": "Unsupported OS"}), 500
        return jsonify({"status": "success", "message": "Folder opened"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to open folder: {e}"}), 500

@app.route('/run_script/<challenge_id>', methods=['POST'])
def run_script(challenge_id):
    mode = session.get("mode", "regular")
    if mode == "solo":
        return jsonify({"status": "error", "message": "Helper scripts are disabled in Solo Mode."}), 403

    challenge_list, _ = load_challenges(mode)
    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    script_path = selectedChallenge.getScript()
    print(f"🚀 Running helper script: {script_path}")

    try:
        subprocess.Popen(['gnome-terminal', '--', 'python3', script_path])
        return jsonify({"status": "success", "message": "Helper script started"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to run script: {e}"}), 500

@app.route('/challenge/<challenge_id>/file/<path:filename>')
def get_challenge_file(challenge_id, filename):
    mode = session.get("mode", "regular")
    if base_mode == "student" and mode == "solo":
        return "File downloads are disabled in Solo Mode.", 403

    challenge_list, _ = load_challenges(mode)
    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return "Challenge not found", 404

    folder = selectedChallenge.getFolder()
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        return "File not found", 404

    print(f"📂 Serving file '{filename}' for challenge {challenge_id}.")
    return send_from_directory(folder, filename)

# === Start Server ===
if __name__ == '__main__':
    print(f"🚀 {base_mode.capitalize()} Hub running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
