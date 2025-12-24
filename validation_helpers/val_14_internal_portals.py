#!/usr/bin/env python3
import sys
import json
import os
import base64
import re
from pathlib import Path

CHALLENGE_ID = "14_InternalPortals"

def load_unlock_data():
    mode = os.environ.get("CCRI_MODE", "guided")
    base_dir = Path(__file__).resolve().parent.parent
    filename = "validation_unlocks_solo.json" if mode == "solo" else "validation_unlocks.json"
    path = base_dir / "web_version_admin" / filename
    
    if not path.exists():
        print(f"❌ Error: Unlock file not found at {path}")
        sys.exit(1)
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data[CHALLENGE_ID]
    except Exception as e:
        print(f"❌ Error loading unlock data: {e}")
        sys.exit(1)

def validate():
    print(f"🕵️  FORENSIC ANALYZER: {CHALLENGE_ID}")
    
    # 1. Get Expected Flag
    unlock_data = load_unlock_data()
    expected_flag = unlock_data["real_flag"]
    print(f"🎯 Expected Flag: {expected_flag}")

    # 2. Find File
    sandbox_path = os.environ.get("CCRI_SANDBOX")
    if sandbox_path:
        challenge_dir = Path(sandbox_path)
    else:
        mode = os.environ.get("CCRI_MODE", "guided")
        folder = "challenges_solo" if mode == "solo" else "challenges"
        challenge_dir = Path(__file__).resolve().parent.parent / folder / CHALLENGE_ID

    server_data_file = challenge_dir / ".server_data"
    if not server_data_file.exists():
        print(f"❌ File missing: {server_data_file}")
        sys.exit(1)

    # 3. Decode
    try:
        b64_content = server_data_file.read_text().strip()
        json_str = base64.b64decode(b64_content).decode("utf-8")
        data_map = json.loads(json_str)
        print(f"✅ Decoded {len(data_map)} portals: {list(data_map.keys())}")
    except Exception as e:
        print(f"❌ Decode failed: {e}")
        sys.exit(1)

    # 4. Search for flag in DOM elements
    # Pattern looks for the flag inside the debug-info span or anywhere in HTML
    found_flags = []
    
    for site, html in data_map.items():
        # Look for our specific hidden span
        if "id='debug-info'" in html or 'id="debug-info"' in html:
            if expected_flag in html:
                print(f"✅ SUCCESS! Exact flag found in hidden span on '{site}'")
                # Print context
                idx = html.find(expected_flag)
                start = max(0, idx - 40)
                end = min(len(html), idx + 40)
                print(f"   Context: ...{html[start:end]}...")
                sys.exit(0)

        # Fallback: check for standard flag pattern anywhere
        flag_pattern = re.compile(r"CCRI-[A-Z0-9]{4}-\d{4}")
        matches = flag_pattern.findall(html)
        for m in matches:
            found_flags.append(f"{site}: {m}")

    # 5. Failure Analysis
    print(f"\n❌ FAILURE: Expected flag {expected_flag} NOT found in any portal.")
    
    if found_flags:
        print(f"⚠️  Detected flag-like strings, but none matched the target:")
        for f in found_flags:
            print(f"   - {f}")
    else:
        print("⚠️  NO flag-like strings found. The DOM injection likely failed.")

    # 6. Dump the HTML of the first site
    first_site = list(data_map.keys())[0]
    print(f"\n📄 DUMP of '{first_site}' (First 500 chars):")
    print("-" * 40)
    print(data_map[first_site][:500])
    print("-" * 40)
    sys.exit(1)

if __name__ == "__main__":
    validate()