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

# === Detect Admin or Student ===
if os.path.basename(server_dir) == "web_version_admin":
    base_mode = "admin"
else:
    base_mode = "student"

print(f"📖 Using template folder at: {template_folder}")
print(f"DEBUG: Base mode = {base_mode}")

# === Simulated Open Ports (dictionaries will be overwritten by generator) ===
GUIDED_FAKE_FLAGS = {
    8051: "CCRI-XIOU-9477",       # ✅ REAL FLAG
    8076: "PJFD-BYXU-9731",       # fake
    8016: "BFRJ-IIKR-1772",       # fake
    8097: "ACBU-6463-XRTN",       # fake
    8045: "WPNG-POKA-4121",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8004: "Welcome to Experimental IoT Server (beta build).",
    8008: "🔒 Unauthorized: API key required.",
    8013: "503 Service Unavailable\nTry again later.",
    8024: "Python HTTP Server: directory listing not allowed.",
    8055: "Hello World!\nTest endpoint active.",
    8064: "System maintenance in progress.",
    8079: "ERROR 400: Bad request syntax.",
    8082: "Error 418: I’m a teapot."
}
GUIDED_SERVICE_NAMES = {
    8004: "omega-stream",
    8008: "beta-hub",
    8013: "metricsd",
    8016: "theta-daemon",
    8024: "sysmon-api",
    8045: "gamma-relay",
    8051: "epsilon-sync",
    8055: "delta-proxy",
    8064: "zeta-cache",
    8076: "configd",
    8079: "kappa-node",
    8082: "delta-sync",
    8097: "auth-service"
}
SOLO_FAKE_FLAGS = {
    9042: "CCRI-MZGP-0820",       # ✅ REAL FLAG
    9051: "UFWC-6488-VRPV",       # fake
    9075: "VIXY-7206-RZNH",       # fake
    9072: "KDOI-7081-HTFP",       # fake
    9024: "YYOV-7146-WHZJ",       # fake
}
SOLO_JUNK_RESPONSES = {
    9001: "Welcome to Experimental IoT Server (beta build).",
    9004: "ERROR 400: Bad request syntax.",
    9007: "🔒 Unauthorized: API key required.",
    9011: "💡 Tip: Scan only the ports you really need.",
    9015: "Server under maintenance.\nPlease retry later.",
    9016: "Hello World!\nTest endpoint active.",
    9020: "403 Forbidden: You don’t have permission to access this resource.",
    9028: "System maintenance in progress.",
    9049: "503 Service Unavailable\nTry again later.",
    9070: "Python HTTP Server: directory listing not allowed.",
    9078: "💻 Dev API v0.1 — POST requests only.",
    9081: "503 Service Unavailable\nTry again later."
}
SOLO_SERVICE_NAMES = {
    9001: "beta-hub",
    9004: "omega-stream",
    9007: "theta-daemon",
    9011: "configd",
    9015: "sysmon-api",
    9016: "metricsd",
    9020: "epsilon-sync",
    9024: "auth-service",
    9028: "kappa-node",
    9042: "delta-sync",
    9049: "delta-sync",
    9051: "update-agent",
    9070: "gamma-relay",
    9072: "delta-proxy",
    9075: "alpha-core",
    9078: "lambda-api",
    9081: "zeta-cache"
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
