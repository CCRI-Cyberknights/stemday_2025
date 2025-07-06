from flask import Flask, render_template, request, jsonify
import subprocess
import json
import os
import socket
import base64

app = Flask(__name__)

# === Hardcoded XOR Key ===
XOR_KEY = "CTF4EVER"

# === Load student challenges.json ===
with open('challenges.json', 'r') as f:
    challenges = json.load(f)

# === Helper: XOR Decode ===
def xor_decode(encoded_base64, key):
    decoded_bytes = base64.b64decode(encoded_base64)
    return ''.join(
        chr(b ^ ord(key[i % len(key)]))
        for i, b in enumerate(decoded_bytes)
    )

# === Routes ===
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
    readme_content = ""
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()

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
        readme=readme_content,
        files=file_list
    )

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
    """Run the helper script in gnome-terminal"""
    if challenge_id not in challenges:
        return jsonify({"status": "error", "message": "Challenge not found"}), 404

    # Resolve absolute paths
    folder = os.path.abspath(challenges[challenge_id]['folder'])
    script = challenges[challenge_id]['script']
    script_path = os.path.join(folder, script)

    if not os.path.exists(script_path):
        return jsonify({"status": "error", "message": "Script not found"}), 404

    try:
        subprocess.Popen([
            'gnome-terminal',
            '--working-directory', folder,
            '--',
            'bash', '-c', f'"{script_path}"; echo "Press ENTER to close..."; read'
        ])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# === Auto-port fallback ===
def get_free_port(preferred_port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', preferred_port)) != 0:
            return preferred_port
        else:
            return 5050

if __name__ == '__main__':
    port = get_free_port()
    print(f"🌐 Student hub running on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)
