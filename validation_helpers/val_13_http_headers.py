#!/usr/bin/env python3
import os
import sys
import json
import base64
from pathlib import Path
try:
    from validation_helpers.common import find_project_root, load_unlock_data, get_ctf_mode
except ImportError:
    # Fallback if running directly from the validation_helpers directory
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from validation_helpers.common import find_project_root, load_unlock_data, get_ctf_mode

CHALLENGE_ID = "13_HTTPHeaders"

def validate_server_data(challenge_dir: Path, expected_flag: str) -> bool:
    data_file = challenge_dir / ".server_data"
    
    if not data_file.exists():
        print(f"❌ Missing challenge data file: {data_file}", file=sys.stderr)
        print("   (Did you run the flag generator script yet?)", file=sys.stderr)
        return False

    try:
        # Read and decode the hidden server configuration
        encoded_content = data_file.read_text(encoding="utf-8").strip()
        decoded_json = base64.b64decode(encoded_content).decode('utf-8')
        data_map = json.loads(decoded_json)

        # Iterate through all generated endpoints (endpoint_1, endpoint_2, etc.)
        for endpoint_name, endpoint_data in data_map.items():
            headers = endpoint_data.get("headers", {})
            
            # Check the specific header where we hide the flag
            x_flag = headers.get("X-Flag")
            
            if x_flag == expected_flag:
                print(f"✅ Found correct flag in {endpoint_name} headers.")
                return True

        print(f"❌ Flag {expected_flag} not found in any endpoint configuration.", file=sys.stderr)
        return False

    except Exception as e:
        print(f"❌ Error parsing server data: {e}", file=sys.stderr)
        return False

def validate(mode="guided", challenge_id=CHALLENGE_ID) -> bool:
    root = find_project_root()
    data = load_unlock_data(root, challenge_id)
    
    if not data:
        print(f"❌ Could not load unlock data for {challenge_id}")
        return False
        
    flag = data.get("real_flag")

    sandbox_override = os.environ.get("CCRI_SANDBOX")
    if sandbox_override:
        challenge_dir = Path(sandbox_override)
    else:
        base_path = "challenges_solo" if mode == "solo" else "challenges"
        challenge_dir = root / base_path / challenge_id

    return validate_server_data(challenge_dir, flag)

if __name__ == "__main__":
    mode = get_ctf_mode()
    success = validate(mode=mode)
    sys.exit(0 if success else 1)