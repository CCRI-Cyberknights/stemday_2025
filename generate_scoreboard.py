import base64
from pathlib import Path

# ==== CONFIGURATION ====

XOR_KEY = "CTF4EVER"
CHALLENGES = {
    "#01 Stego": "CCRI-STE-101",
    "#02 Base64": "CCRI-B64-102",
    "#03 ROT13": "CCRI-ROT-303",
    "#04 Vigenère": "CCRI-VIG-004",
    # ... add more as needed
}

# ==== XOR + BASE64 OBFUSCATION ====

def xor_encrypt(plain, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(plain))

def make_obfuscated_flags(flags, key):
    return {
        chal: base64.b64encode(xor_encrypt(flag, key).encode()).decode()
        for chal, flag in flags.items()
    }

# ==== HTML GENERATION ====

def make_html(challenges, obfuscated_flags, key_b64):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CCRI CTF Flag Tracker</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 20px; }}
        h1 {{ text-align: center; }}
        #challenges {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 20px; }}
        .challenge {{ background: #fff; padding: 10px; border-radius: 5px; box-shadow: 0 0 5px #ccc; }}
        .complete input {{ background-color: #d4edda; }}
        input[type="text"] {{ width: 90%; padding: 5px; }}
        .status {{ font-weight: bold; margin-left: 5px; }}
    </style>
</head>
<body>
    <h1>CCRI CTF Flag Tracker</h1>
    <p>Enter the flag you found for each challenge below. Your progress will be saved automatically in your browser.</p>
    <p><strong>Flag Format:</strong> CCRI-XXX-###</p>
    <h2 id="progress">0 of {len(challenges)} challenges completed</h2>

    <div id="challenges">
"""

    for name in challenges:
        html += f"""        <div class="challenge" id="{name}-container">
            <label for="{name}"><strong>{name}</strong></label><br>
            <input type="text" id="{name}" oninput="validate('{name}')">
            <span class="status" id="{name}-status"></span>
        </div>\n"""

    html += """    </div>\n
    <script>
        const xorKeyBase64 = \"""" + key_b64 + """\";
        const xorKey = atob(xorKeyBase64);

        const correctFlags = {\n"""

    for name, obf in obfuscated_flags.items():
        html += f'            "{name}": "{obf}",\n'

    html += """        };

        function xorDecrypt(encodedBase64, key) {
            const data = atob(encodedBase64);
            let result = '';
            for (let i = 0; i < data.length; i++) {
                result += String.fromCharCode(data.charCodeAt(i) ^ key.charCodeAt(i % key.length));
            }
            return result;
        }

        function updateProgress() {
            let complete = 0;
            Object.keys(correctFlags).forEach(id => {
                const input = document.getElementById(id);
                const stored = localStorage.getItem(id);
                const container = document.getElementById(id + "-container");
                const status = document.getElementById(id + "-status");
                const correct = xorDecrypt(correctFlags[id], xorKey);
                if (stored && stored.toUpperCase() === correct) {
                    input.value = stored;
                    container.classList.add("complete");
                    status.textContent = "✓ Correct";
                    complete++;
                } else {
                    container.classList.remove("complete");
                    status.textContent = "";
                }
            });
            document.getElementById("progress").textContent = complete + " of """ + str(len(challenges)) + """ challenges completed";
        }

        function validate(id) {
            const input = document.getElementById(id);
            const value = input.value.trim().toUpperCase();
            localStorage.setItem(id, value);
            updateProgress();
        }

        window.onload = () => {
            Object.keys(correctFlags).forEach(id => {
                const input = document.getElementById(id);
                const stored = localStorage.getItem(id);
                if (stored) {
                    input.value = stored;
                }
            });
            updateProgress();
        };
    </script>
</body>
</html>
"""
    return html

# ==== MAIN EXECUTION ====

def main():
    obfuscated_flags = make_obfuscated_flags(CHALLENGES, XOR_KEY)
    key_b64 = base64.b64encode(XOR_KEY.encode()).decode()
    html = make_html(CHALLENGES, obfuscated_flags, key_b64)
    Path("index_grid_obfuscated.html").write_text(html)
    print("[+] HTML scoreboard generated: index_grid_obfuscated.html")

if __name__ == "__main__":
    main()
