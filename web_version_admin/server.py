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
            'bash', script_path
        ])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# === Simulated Open Ports (Challenge #17) ===
FAKE_FLAGS = {
    8004: "NMAP-PORT-4312",       # fake
    8023: "SCAN-4312-PORT",       # fake
    8047: "CCRI-SCAN-8472",       # ✅ REAL FLAG
    8072: "OPEN-SERVICE-9281",    # fake
    8095: "HTTP-7721-SERVER"      # fake
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

@app.route('/ports/<int:port>')
def simulate_ports(port):
    """Simulate open ports for Nmap Scan Puzzle"""
    if port in FAKE_FLAGS:
        return FAKE_FLAGS[port]
    elif port in JUNK_RESPONSES:
        return JUNK_RESPONSES[port]
    else:
        return "Connection refused", 404

if __name__ == '__main__':
    print("🌐 Student hub running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)

