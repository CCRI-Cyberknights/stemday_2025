import os
import sys
import json
from pathlib import Path

def find_project_root() -> Path:
    dir_path = Path(__file__).resolve().parent
    while dir_path != Path("/"):
        if (dir_path / ".ccri_ctf_root").exists():
            return dir_path
        dir_path = dir_path.parent
    print("❌ ERROR: Could not find .ccri_ctf_root", file=sys.stderr)
    sys.exit(1)

def get_ctf_mode() -> str:
    env = os.environ.get("CCRI_MODE")
    if env in ("guided", "solo"):
        return env
    return "guided"  # Default to guided if not explicitly set

def load_unlock_data(project_root: Path, challenge_id: str) -> dict:
    mode = get_ctf_mode()
    filename = "validation_unlocks_solo.json" if mode == "solo" else "validation_unlocks.json"
    path = project_root / "web_version_admin" / filename
    if not path.exists():
        print(f"❌ Unlock file missing: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f).get(challenge_id, {})

def load_flag(project_root: Path, challenge_id: str) -> str:
    return load_unlock_data(project_root, challenge_id).get("real_flag", "")

def get_challenge_file(project_root: Path, challenge_id: str, unlock_data: dict) -> Path:
    mode = get_ctf_mode()
    if mode == "guided":
        file_rel = unlock_data.get("challenge_file", f"challenges/{challenge_id}/encoded.txt")
    else:
        file_rel = f"challenges_solo/{challenge_id}/encoded.txt"
    return project_root / file_rel
