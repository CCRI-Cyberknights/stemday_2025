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

sys.dont_write_bytecode = True  # 🛡 prevent .pyc files in admin

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

# === Simulated Open Ports ===
# Guided Mode: 8000–8100
GUIDED_FAKE_FLAGS = {
    8005: "CCRI-HVDF-4036",       # ✅ REAL FLAG
    8024: "CTAU-3189-ZWJC",       # fake
    8072: "HKJP-OWWV-3721",       # fake
    8056: "ZLND-WYOY-4908",       # fake
    8041: "AOFB-9291-NAFM",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8001: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    8009: "🔒 Unauthorized: API key required.",
    8015: "503 Service Unavailable\nTry again later.",
    8020: "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>",
}
GUIDED_SERVICE_NAMES = {
    8001: "dev-http",
    8005: "kappa-node",
    8024: "lambda-api",
    8072: "gamma-relay",
    8056: "beta-hub",
    8041: "metricsd",
}

# Solo Mode: 9000–9100
SOLO_FAKE_FLAGS = {
    9005: "CCRI-QWER-7890",       # ✅ REAL FLAG
    9024: "ASDF-1234-HJKL",       # fake
    9072: "ZXCV-5678-UIOP",       # fake
    9056: "BNMM-0987-LKJH",       # fake
    9041: "YTRE-4567-WQAS",       # fake
}
SOLO_JUNK_RESPONSES = {
    9001: "Welcome to Solo Dev Server v2.0\nAuthentication required.",
    9009: "🔒 Solo API key missing.",
    9015: "503 Solo Service Unavailable\nTry again later.",
    9020: "<html><body><h1>Solo It works!</h1><p>Default page.</p></body></html>",
}
SOLO_SERVICE_NAMES = {
    9001: "solo-http",
    9005: "sigma-node",
    9024: "tau-api",
    9072: "delta-relay",
    9056: "omega-hub",
    9041: "solo-metricsd",
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
        print(f"🛰️  Simulated service running on port {port} ({service_map.get(port, 'http')})")
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
    """
    Load challenges from the correct JSON file based on mode.
    """
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

    # Dynamic title for Challenge List
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


# === Route: Open Folder ===
@app.route('/open_folder/<challenge_id>', methods=['POST'])
def open_folder(challenge_id):
    """
    Open the challenge folder in the system file explorer (works in all modes).
    """
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


# === Route: Run Helper Script ===
@app.route('/run_script/<challenge_id>', methods=['POST'])
def run_script(challenge_id):
    """
    Run the guided helper script for the challenge (disabled in Solo mode).
    """
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


# === Route: Serve Challenge Files ===
@app.route('/challenge/<challenge_id>/file/<path:filename>')
def get_challenge_file(challenge_id, filename):
    """
    Serve individual challenge files.
    Active in Admin and Guided (regular) modes.
    """
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
