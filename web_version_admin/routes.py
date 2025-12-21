try:
    from flask import Blueprint, render_template, request, jsonify, Markup, send_from_directory, redirect, url_for, session
except ImportError:
    from flask import Blueprint, render_template, request, jsonify, send_from_directory, redirect, url_for, session
    from markupsafe import Markup

import os
import sys
import subprocess
import markdown
import config
from utils import load_challenges

bp = Blueprint('main', __name__, static_folder=config.static_folder, static_url_path='/static')

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
        # Graceful redirect to whatever exists
        if config.DEFAULT_MODE:
            print(f"⚠️ Requested mode '{mode}' not available. Redirecting to {config.DEFAULT_MODE}.")
            session["mode"] = config.DEFAULT_MODE
            return redirect(url_for('main.index'))
        return "No challenges available in this build.", 404
    session["mode"] = mode
    print(f"🌐 Mode set to: {mode.upper()}")
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
        print(f"❌ ERROR loading challenges: {e}")
        return render_template(
            'error.html',
            message="No challenges available in this build."
        ), 404

    if config.base_mode == "admin":
        list_title = f"Admin {'Exploration' if mode == 'regular' else 'Solo'} Challenge List"
    else:
        list_title = f"Student {'Exploration' if mode == 'regular' else 'Solo'} Challenge List"

    print(f"📄 Opening {list_title}...")
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

    # === MODIFICATION START ===
    # Scripts that should be visible to students for debugging/fixing
    visible_scripts = ["broken_flag.py"]

    file_list = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and f != "README.md"
        and not f.startswith(".")
        # Allow files that are NOT python scripts OR are in the visible_scripts list
        and (not f.endswith(".py") or f in visible_scripts)
    ]
    # === MODIFICATION END ===

    template = "challenge_solo.html" if mode == "solo" else "challenge.html"
    print(f"➡️ Opening {selectedChallenge.getName()} in {mode.upper()} mode.")
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
        print(f"✅ Correct flag submitted for {challenge_id}")
        return jsonify({"status": "correct"})
    else:
        print(f"❌ Incorrect flag submitted for {challenge_id}")
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
    print(f"🚀 Running helper script: {script_path}")

    try:
        subprocess.Popen(['gnome-terminal', '--', 'python3', script_path])
        return jsonify({"status": "success", "message": "Helper script started"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to run script: {e}"}), 500

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

    print(f"📂 Serving file '{filename}' for challenge {challenge_id}.")
    return send_from_directory(folder, filename)

@bp.route("/linux-basics")
def linux_basics():
    return render_template("linux_basics.html")

@bp.route('/healthz')
def healthz():
    return jsonify({
        "available_modes": config.AVAILABLE_MODES,
        "default_mode": config.DEFAULT_MODE,
        "guided_present": os.path.isdir(config.GUIDED_DIR),
        "solo_present": os.path.isdir(config.SOLO_DIR),
        "server_dir": config.server_dir,
        "base_dir": config.BASE_DIR,
        "assets_env": os.environ.get("CCRI_ASSETS_DIR"),
        "argv0": sys.argv[0],
    })