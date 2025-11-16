try:
    from flask import Flask, render_template, request, jsonify, Markup, send_from_directory, redirect, url_for, session
except ImportError:
    from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
    from markupsafe import Markup

import os, sys, json, threading, logging, subprocess, base64, markdown
from http.server import BaseHTTPRequestHandler, HTTPServer

# ---------- PATH RESOLUTION (only place we decide paths) ----------
ASSETS_DIR_OVERRIDE = os.environ.get("CCRI_ASSETS_DIR")

def detect_assets_dir():
    """
    Priority:
      1) CCRI_ASSETS_DIR (env)
      2) <dir_of_running_pyz>/web_version (next to the pyz)
      3) directory of this source file (dev/admin tree)
    """
    if ASSETS_DIR_OVERRIDE:
        return os.path.abspath(ASSETS_DIR_OVERRIDE)

    pyz_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    candidate = os.path.join(pyz_dir, "web_version")
    if os.path.isdir(candidate):
        return candidate

    return os.path.dirname(os.path.abspath(__file__))

server_dir = detect_assets_dir()
BASE_DIR   = os.path.abspath(os.path.join(server_dir, ".."))
# ---------------------------------------------------------------

sys.dont_write_bytecode = True

# Make sure we can import Challenge/ChallengeList from BASE_DIR
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ChallengeList import ChallengeList

template_folder = os.path.join(server_dir, "templates")
static_folder   = os.path.join(server_dir, "static")

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = "super_secret_key"

DEBUG_MODE = os.environ.get("CCRI_DEBUG", "0") == "1"
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)

# Mode selection
base_mode = os.environ.get("CCRI_CTF_MODE", "").strip().lower()
if not base_mode:
    base_mode = "admin" if os.path.basename(server_dir) == "web_version_admin" else "student"

has_admin = os.path.isdir(os.path.join(BASE_DIR, "web_version_admin"))
if base_mode == "admin" and not has_admin:
    print("⚠️ Admin mode requested but admin assets missing; forcing STUDENT mode.")
    base_mode = "student"

os.environ["CCRI_CTF_MODE"] = base_mode

print(f"📖 Using template folder at: {template_folder}")
print(f"DEBUG: Base mode = {base_mode}")

# Folders containing challenge data
GUIDED_DIR = os.path.join(BASE_DIR, "challenges")
SOLO_DIR   = os.path.join(BASE_DIR, "challenges_solo")

def detect_available_modes():
    modes = []
    if os.path.isdir(GUIDED_DIR):
        modes.append("regular")
    if os.path.isdir(SOLO_DIR):
        modes.append("solo")
    return modes

AVAILABLE_MODES = detect_available_modes()
DEFAULT_MODE = "regular" if "regular" in AVAILABLE_MODES else ("solo" if "solo" in AVAILABLE_MODES else None)
print(f"🧭 AVAILABLE_MODES = {AVAILABLE_MODES} | DEFAULT_MODE = {DEFAULT_MODE}")

# === Simulated Open Ports (dictionaries will be overwritten by generator) ===
GUIDED_FAKE_FLAGS = {
    8017: "CCRI-SNTD-5752",       # ✅ REAL FLAG
    8074: "KZQH-8026-ITIQ",       # fake
    8057: "KZGI-7747-ZQTP",       # fake
    8032: "OUFZ-KVBG-5536",       # fake
    8024: "KOUA-3677-IVJH",       # fake
}
GUIDED_JUNK_RESPONSES = {
    8015: "Welcome to Experimental IoT Server (beta build).",
    8025: "🔒 Unauthorized: API key required.",
    8028: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    8031: "System maintenance in progress.",
    8037: "Welcome to Experimental IoT Server (beta build).",
    8050: "Error 418: I’m a teapot.",
    8059: "Welcome to Dev HTTP Server v1.3\nPlease login to continue.",
    8085: "403 Forbidden: You don’t have permission to access this resource.",
    8096: "Hello World!\nTest endpoint active."
}
GUIDED_SERVICE_NAMES = {
    8015: "epsilon-sync",
    8017: "theta-daemon",
    8024: "update-agent",
    8025: "alpha-core",
    8028: "sysmon-api",
    8031: "gamma-relay",
    8032: "beta-hub",
    8037: "configd",
    8050: "zeta-cache",
    8057: "metricsd",
    8059: "delta-proxy",
    8074: "auth-service",
    8085: "kappa-node",
    8096: "omega-stream"
}
SOLO_FAKE_FLAGS = {
    9098: "CCRI-OIRR-8437",       # ✅ REAL FLAG
    9030: "TPYU-JWRL-7275",       # fake
    9093: "YRNA-HQLV-0256",       # fake
    9053: "UUNZ-WKRS-1755",       # fake
    9019: "YKAZ-XHWU-1229",       # fake
}
SOLO_JUNK_RESPONSES = {
    9001: "403 Forbidden: You don’t have permission to access this resource.",
    9003: "Welcome to Experimental IoT Server (beta build).",
    9018: "Python HTTP Server: directory listing not allowed.",
    9034: "503 Service Unavailable\nTry again later.",
    9046: "ERROR 400: Bad request syntax.",
    9050: "ERROR 400: Bad request syntax.",
    9070: "<html><body><h1>It works!</h1><p>Apache2 default page.</p></body></html>",
    9077: "Error 418: I’m a teapot.",
    9078: "Server under maintenance.\nPlease retry later.",
    9083: "503 Service Unavailable\nTry again later.",
    9092: "💡 Tip: Scan only the ports you really need."
}
SOLO_SERVICE_NAMES = {
    9001: "sysmon-api",
    9003: "lambda-api",
    9018: "delta-proxy",
    9019: "gamma-relay",
    9030: "beta-hub",
    9034: "kappa-node",
    9046: "theta-daemon",
    9050: "epsilon-sync",
    9053: "update-agent",
    9070: "omega-stream",
    9077: "metricsd",
    9078: "zeta-cache",
    9083: "alpha-core",
    9092: "delta-sync",
    9093: "configd",
    9098: "auth-service"
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

# === Start Simulated Services (only for present modes) ===
def start_fake_service(port, response_map, service_map):
    try:
        server = HTTPServer(('0.0.0.0', port), PortHandlerFactory(response_map, service_map))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"🚁️  Simulated service running on port {port} ({service_map.get(port, 'http')})")
    except OSError as e:
        print(f"❌ Could not bind port {port}: {e}")

if "regular" in AVAILABLE_MODES:
    for port in GUIDED_ALL_PORTS.keys():
        start_fake_service(port, GUIDED_ALL_PORTS, GUIDED_SERVICE_NAMES)

if "solo" in AVAILABLE_MODES:
    for port in SOLO_ALL_PORTS.keys():
        start_fake_service(port, SOLO_ALL_PORTS, SOLO_SERVICE_NAMES)

# === Helper: Load Challenges (folder-aware & graceful fallback) ===
def load_challenges(mode=None):
    """
    Returns (ChallengeList, challenges_folder_name)
    Tries requested mode, falls back to DEFAULT_MODE, then tries the 'other' mode before failing.
    """
    # normalize and guard
    if mode not in ("regular", "solo"):
        mode = DEFAULT_MODE

    # If requested mode isn't available, use default
    if mode not in AVAILABLE_MODES:
        mode = DEFAULT_MODE

    if mode is None:
        raise FileNotFoundError("No challenges folders present.")

    if mode == "solo":
        challenges_path = os.path.join(server_dir, "challenges_solo.json")
        challenges_folder = "challenges_solo"
        other_mode = "regular"
        other_path = os.path.join(server_dir, "challenges.json")
    else:
        challenges_path = os.path.join(server_dir, "challenges.json")
        challenges_folder = "challenges"
        other_mode = "solo"
        other_path = os.path.join(server_dir, "challenges_solo.json")

    print(f"📖 Loading {mode.upper()} challenges from {challenges_path}")

    try:
        challenge_list = ChallengeList(challenges_file=challenges_path)
        list_type = "Guided" if mode == "regular" else "Solo"
        user_type = "Admin" if base_mode == "admin" else "Student"
        print(f"✅ {user_type} {list_type} Challenge List loaded ({challenge_list.numOfChallenges} challenges).")
        return challenge_list, challenges_folder
    except (FileNotFoundError, json.JSONDecodeError) as err:
        print(f"⚠️ {err.__class__.__name__}: {err}")
        # Try the other mode if its folder is present
        if other_mode in AVAILABLE_MODES and os.path.exists(other_path):
            print(f"↪️ Falling back to {other_mode.upper()} due to missing/invalid JSON.")
            return load_challenges(other_mode)
        # Final fail
        raise

# === Flask Routes ===
@app.route('/')
def landing_page():
    # Choose sane default for the session based on what's present
    session.setdefault("mode", DEFAULT_MODE if DEFAULT_MODE else "regular")

    # Load optional Markdown welcome text from /static/welcome.md
    welcome_md_path = os.path.join(app.static_folder, "welcome.md")
    if os.path.exists(welcome_md_path):
        with open(welcome_md_path, "r", encoding="utf-8") as f:
            welcome_html = Markup(markdown.markdown(
                f.read(),
                extensions=["fenced_code", "sane_lists", "tables"]
            ))
    else:
        welcome_html = Markup("<p><em>No welcome text found.</em></p>")

    print(f"🌐 {base_mode.capitalize()} Hub loaded at http://127.0.0.1:5000")
    return render_template(
        'landing.html',
        base_mode=base_mode,
        welcome_html=welcome_html,
        available_modes=AVAILABLE_MODES,
        default_mode=DEFAULT_MODE
    )

@app.route('/set_mode/<mode>')
def set_mode(mode):
    if mode not in ["regular", "solo"]:
        return "Invalid mode", 400
    if mode not in AVAILABLE_MODES:
        # Graceful redirect to whatever exists
        if DEFAULT_MODE:
            print(f"⚠️ Requested mode '{mode}' not available. Redirecting to {DEFAULT_MODE}.")
            session["mode"] = DEFAULT_MODE
            return redirect(url_for('index'))
        return "No challenges available in this build.", 404
    session["mode"] = mode
    print(f"🌐 Mode set to: {mode.upper()}")
    return redirect(url_for('index'))

@app.route('/challenges')
def index():
    mode = session.get("mode", DEFAULT_MODE if DEFAULT_MODE else "regular")
    if mode not in AVAILABLE_MODES:
        mode = DEFAULT_MODE
        session["mode"] = mode

    try:
        challenge_list, challenges_folder = load_challenges(mode)
    except Exception as e:
        print(f"❌ ERROR loading challenges: {e}")
        return render_template(
            'error.html',
            message="No challenges available in this build."
        ), 404

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
    mode = session.get("mode", DEFAULT_MODE if DEFAULT_MODE else "regular")
    if mode not in AVAILABLE_MODES:
        mode = DEFAULT_MODE
        session["mode"] = mode

    try:
        challenge_list, challenges_folder = load_challenges(mode)
    except Exception as e:
        return render_template('error.html', message=str(e)), 404

    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        # Try the other mode before 404
        other = "solo" if mode == "regular" else "regular"
        if other in AVAILABLE_MODES:
            try:
                other_list, _ = load_challenges(other)
                selectedChallenge = other_list.get_challenge_by_id(challenge_id)
                if selectedChallenge:
                    return redirect(url_for('challenge_view', challenge_id=challenge_id) + f"?mode={other}")
            except Exception:
                pass
        return "Challenge not found", 404

    folder = selectedChallenge.getFolder()
    if not os.path.exists(folder):
        # Try other mode's folder before 404
        other = "solo" if mode == "regular" else "regular"
        if other in AVAILABLE_MODES:
            try:
                other_list, _ = load_challenges(other)
                sc_other = other_list.get_challenge_by_id(challenge_id)
                if sc_other and os.path.exists(sc_other.getFolder()):
                    session["mode"] = other
                    return redirect(url_for('challenge_view', challenge_id=challenge_id))
            except Exception:
                pass
        return f"⚠️ Challenge folder not found: {folder}", 404

    readme_html = ""
    readme_path = os.path.join(folder, 'README.md')
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                raw_readme = f.read()
                readme_html = Markup(markdown.markdown(raw_readme, extensions=["tables"]))
        except Exception as e:
            readme_html = f"<p><strong>Error loading README.md:</strong> {e}</p>"

    file_list = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and f != "README.md"
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
    mode = session.get("mode", DEFAULT_MODE if DEFAULT_MODE else "regular")
    try:
        challenge_list, _ = load_challenges(mode)
    except Exception:
        return jsonify({"status": "error", "message": "No challenges available"}), 404

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
    mode = session.get("mode", DEFAULT_MODE if DEFAULT_MODE else "regular")
    try:
        challenge_list, _ = load_challenges(mode)
    except Exception:
        return jsonify({"status": "error", "message": "No challenges available"}), 404

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
    mode = session.get("mode", DEFAULT_MODE if DEFAULT_MODE else "regular")
    if mode == "solo":
        return jsonify({"status": "error", "message": "Helper scripts are disabled in Solo Mode."}), 403

    try:
        challenge_list, _ = load_challenges(mode)
    except Exception:
        return jsonify({"status": "error", "message": "No challenges available"}), 404

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
    mode = session.get("mode", DEFAULT_MODE if DEFAULT_MODE else "regular")
    try:
        challenge_list, _ = load_challenges(mode)
    except Exception:
        return "No challenges available", 404

    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return "Challenge not found", 404

    folder = selectedChallenge.getFolder()
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        return "File not found", 404

    print(f"📂 Serving file '{filename}' for challenge {challenge_id}.")
    return send_from_directory(folder, filename)

@app.route("/linux-basics")
def linux_basics():
    return render_template("linux_basics.html")

@app.route('/healthz')
def healthz():
    return jsonify({
        "available_modes": AVAILABLE_MODES,
        "default_mode": DEFAULT_MODE,
        "guided_present": os.path.isdir(GUIDED_DIR),
        "solo_present": os.path.isdir(SOLO_DIR),
        "server_dir": server_dir,
        "base_dir": BASE_DIR,
        "assets_env": os.environ.get("CCRI_ASSETS_DIR"),
        "argv0": sys.argv[0],
    })

# DO NOT auto-run here; __main__.py will run app.run()

# === Start Server ===
if __name__ == '__main__':
    print(f"🚀 {base_mode.capitalize()} Hub running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
