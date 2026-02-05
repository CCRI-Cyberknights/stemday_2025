try:
    from flask import Blueprint, render_template, request, jsonify, Markup, send_from_directory, redirect, url_for, session, make_response
except ImportError:
    from flask import Blueprint, render_template, request, jsonify, send_from_directory, redirect, url_for, session, make_response
    from markupsafe import Markup

import os
import sys
import subprocess
import markdown
import json
import base64
import config
from utils import load_challenges

bp = Blueprint('main', __name__, static_folder=config.static_folder, static_url_path='/static')

# --- Helper to read HIDDEN/OBFUSCATED challenge files ---
def get_challenge_server_data(challenge_id, mode_override=None):
    """
    Locates the hidden .server_data file, base64 decodes it, and returns the JSON dict.
    Allows forcing a specific mode (e.g. for unique Solo routes).
    """
    if mode_override:
        mode = mode_override
    else:
        mode = session.get("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")
        
    try:
        challenge_list, _ = load_challenges(mode)
        # Ensure we pass the ID as a string exactly as it appears in challenges.json
        challenge = challenge_list.get_challenge_by_id(str(challenge_id))
        if challenge:
            path = os.path.join(challenge.getFolder(), ".server_data")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    encoded_content = f.read().strip()
                    decoded_json = base64.b64decode(encoded_content).decode('utf-8')
                    return json.loads(decoded_json)
    except Exception as e:
        print(f"Error reading server data for challenge {challenge_id} (Mode: {mode}): {e}")
    return None

@bp.route('/')
def landing_page():
    # Choose sane default for the session based on what's present
    session.setdefault("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")

    # Load optional Markdown welcome text from /static/welcome.md
    welcome_md_path = os.path.join(config.static_folder, "welcome.md")
    if os.path.exists(welcome_md_path):
        with open(welcome_md_path, "r", encoding="utf-8") as f:
            welcome_html = Markup(markdown.markdown(
                f.read(),
                extensions=["fenced_code", "sane_lists", "tables"]
            ))
    else:
        welcome_html = Markup("<p><em>No welcome text found.</em></p>")

    return render_template(
        'landing.html',
        base_mode=config.base_mode,
        welcome_html=welcome_html,
        available_modes=config.AVAILABLE_MODES,
        default_mode=config.DEFAULT_MODE
    )

@bp.route('/set_mode/<mode>')
def set_mode(mode):
    if mode not in ["regular", "solo"]:
        return "Invalid mode", 400
    if mode not in config.AVAILABLE_MODES:
        if config.DEFAULT_MODE:
            session["mode"] = config.DEFAULT_MODE
            return redirect(url_for('main.index'))
        return "No challenges available in this build.", 404
    session["mode"] = mode
    return redirect(url_for('main.index'))

@bp.route('/challenges')
def index():
    mode = session.get("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")
    if mode not in config.AVAILABLE_MODES:
        mode = config.DEFAULT_MODE
        session["mode"] = mode

    try:
        challenge_list, challenges_folder = load_challenges(mode)
    except Exception as e:
        return render_template('error.html', message="No challenges available in this build."), 404

    if config.base_mode == "admin":
        list_title = f"Admin {'Exploration' if mode == 'regular' else 'Solo'} Challenge List"
    else:
        list_title = f"Student {'Exploration' if mode == 'regular' else 'Solo'} Challenge List"

    return render_template('index.html',
                           challenges=challenge_list,
                           base_mode=config.base_mode,
                           mode=mode,
                           list_title=list_title)

@bp.route('/challenge/<challenge_id>')
def challenge_view(challenge_id):
    mode = session.get("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")
    if mode not in config.AVAILABLE_MODES:
        mode = config.DEFAULT_MODE
        session["mode"] = mode

    try:
        challenge_list, challenges_folder = load_challenges(mode)
    except Exception as e:
        return render_template('error.html', message=str(e)), 404

    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        # Try the other mode before 404
        other = "solo" if mode == "regular" else "regular"
        if other in config.AVAILABLE_MODES:
            try:
                other_list, _ = load_challenges(other)
                selectedChallenge = other_list.get_challenge_by_id(challenge_id)
                if selectedChallenge:
                    return redirect(url_for('main.challenge_view', challenge_id=challenge_id) + f"?mode={other}")
            except Exception:
                pass
        return "Challenge not found", 404

    folder = selectedChallenge.getFolder()
    if not os.path.exists(folder):
         # Try other mode's folder before 404
        other = "solo" if mode == "regular" else "regular"
        if other in config.AVAILABLE_MODES:
            try:
                other_list, _ = load_challenges(other)
                sc_other = other_list.get_challenge_by_id(challenge_id)
                if sc_other and os.path.exists(sc_other.getFolder()):
                    session["mode"] = other
                    return redirect(url_for('main.challenge_view', challenge_id=challenge_id))
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

    # Scripts that should be visible to students for debugging/fixing
    visible_scripts = ["broken_flag.py"]

    file_list = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and f != "README.md"
        and not f.startswith(".")
        and (not f.endswith(".py") or f in visible_scripts)
        and f != ".server_data" 
    ]

    template = "challenge_solo.html" if mode == "solo" else "challenge.html"
    return render_template(template,
                           challenge=selectedChallenge,
                           readme=readme_html,
                           files=file_list,
                           base_mode=config.base_mode,
                           mode=mode)

@bp.route('/submit_flag/<challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    mode = session.get("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")
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
        return jsonify({"status": "correct"})
    else:
        return jsonify({"status": "incorrect"})

@bp.route('/open_folder/<challenge_id>', methods=['POST'])
def open_folder(challenge_id):
    mode = session.get("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")
    try:
        challenge_list, _ = load_challenges(mode)
    except Exception:
        return jsonify({"status": "error", "message": "No challenges available"}), 404

    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    folder_path = selectedChallenge.getFolder()
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

@bp.route('/run_script/<challenge_id>', methods=['POST'])
def run_script(challenge_id):
    mode = session.get("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")
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
    try:
        subprocess.Popen(['gnome-terminal', '--', 'python3', script_path])
        return jsonify({"status": "success", "message": "Helper script started"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to run script: {e}"}), 500

@bp.route('/run_coach/<challenge_id>', methods=['POST'])
def run_coach(challenge_id):
    mode = session.get("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")
    try:
        challenge_list, _ = load_challenges(mode)
    except Exception:
        return jsonify({"status": "error", "message": "No challenges available"}), 404

    selectedChallenge = challenge_list.get_challenge_by_id(challenge_id)
    if selectedChallenge is None:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    script_path = os.path.join(selectedChallenge.getFolder(), '.coach.py')
    if not os.path.exists(script_path):
        return jsonify({"status": "error", "message": "Coach script not found for this challenge."}), 404

    try:
        subprocess.Popen([
            "mate-terminal",
            "--geometry=90x35+50+100",
            "--title=Coach Mode: " + selectedChallenge.getName(),
            "--",
            "python3", script_path
        ])
        return jsonify({"status": "success", "message": "Coach terminal launched"})
    except FileNotFoundError:
        try:
             subprocess.Popen([
                "x-terminal-emulator",
                "-e", f"python3 {script_path}"
            ])
             return jsonify({"status": "success", "message": "Coach terminal launched (fallback)"})
        except Exception as e:
             return jsonify({"status": "error", "message": f"Terminal not found: {e}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to run coach: {e}"}), 500

@bp.route('/challenge/<challenge_id>/file/<path:filename>')
def get_challenge_file(challenge_id, filename):
    mode = session.get("mode", config.DEFAULT_MODE if config.DEFAULT_MODE else "regular")
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
    return send_from_directory(folder, filename)

# ==========================================
#  CHALLENGE 13: HTTP Headers Mystery
# ==========================================

# --- REGULAR MODE (Coach/Explore) ---
# Uses /mystery/endpoint_X and keys "endpoint_X"
def serve_header_challenge(index, mode_override=None, key_prefix="endpoint"):
    data_map = get_challenge_server_data("13_HTTPHeaders", mode_override=mode_override)
    endpoint_key = f"{key_prefix}_{index}"

    if not data_map or endpoint_key not in data_map:
        return make_response("System Error: Challenge data missing or invalid mode.", 404)

    data = data_map[endpoint_key]
    resp = make_response(data.get("body", ""), data.get("status_code", 200))
    for k, v in data.get("headers", {}).items():
        resp.headers[k] = v
    return resp

@bp.route('/mystery/endpoint_1')
def header_mystery_1(): return serve_header_challenge(1, mode_override="regular")
@bp.route('/mystery/endpoint_2')
def header_mystery_2(): return serve_header_challenge(2, mode_override="regular")
@bp.route('/mystery/endpoint_3')
def header_mystery_3(): return serve_header_challenge(3, mode_override="regular")
@bp.route('/mystery/endpoint_4')
def header_mystery_4(): return serve_header_challenge(4, mode_override="regular")
@bp.route('/mystery/endpoint_5')
def header_mystery_5(): return serve_header_challenge(5, mode_override="regular")

# --- SOLO MODE ---
# Uses /covert/channel_X and keys "channel_X"
@bp.route('/covert/channel_1')
def solo_header_mystery_1(): return serve_header_challenge(1, mode_override="solo", key_prefix="channel")
@bp.route('/covert/channel_2')
def solo_header_mystery_2(): return serve_header_challenge(2, mode_override="solo", key_prefix="channel")
@bp.route('/covert/channel_3')
def solo_header_mystery_3(): return serve_header_challenge(3, mode_override="solo", key_prefix="channel")
@bp.route('/covert/channel_4')
def solo_header_mystery_4(): return serve_header_challenge(4, mode_override="solo", key_prefix="channel")
@bp.route('/covert/channel_5')
def solo_header_mystery_5(): return serve_header_challenge(5, mode_override="solo", key_prefix="channel")


# ==========================================
#  CHALLENGE 14: Internal Portals
# ==========================================

# --- REGULAR MODE (Coach/Explore) ---
# Uses /internal/<site_name>
@bp.route('/internal/<site_name>')
def internal_sites(site_name):
    site_name = site_name.lower()
    data_map = get_challenge_server_data("14_InternalPortals", mode_override="regular")
    if data_map and site_name in data_map:
        return data_map[site_name]
    return "404 - Site Not Found", 404

# --- SOLO MODE ---
# Uses /private/<site_name>
@bp.route('/private/<site_name>')
def solo_internal_sites(site_name):
    site_name = site_name.lower()
    # Force load from Solo data
    data_map = get_challenge_server_data("14_InternalPortals", mode_override="solo")
    if data_map and site_name in data_map:
        return data_map[site_name]
    return "404 - Restricted Sector Not Found", 404

@bp.route("/linux-basics")
def linux_basics():
    return render_template("linux_basics.html")

@bp.route('/healthz')
def healthz():
    return jsonify({
        "status": "ok",
        "mode": session.get("mode", "unknown")
    })