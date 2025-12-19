import os
import sys
import json
import config

# Ensure we can import ChallengeList from BASE_DIR
if config.BASE_DIR not in sys.path:
    sys.path.insert(0, config.BASE_DIR)

from ChallengeList import ChallengeList

def load_challenges(mode=None):
    """
    Returns (ChallengeList, challenges_folder_name)
    Tries requested mode, falls back to DEFAULT_MODE, then tries the 'other' mode before failing.
    """
    # normalize and guard
    if mode not in ("regular", "solo"):
        mode = config.DEFAULT_MODE

    # If requested mode isn't available, use default
    if mode not in config.AVAILABLE_MODES:
        mode = config.DEFAULT_MODE

    if mode is None:
        raise FileNotFoundError("No challenges folders present.")

    if mode == "solo":
        challenges_path = os.path.join(config.server_dir, "challenges_solo.json")
        challenges_folder = "challenges_solo"
        other_mode = "regular"
        other_path = os.path.join(config.server_dir, "challenges.json")
    else:
        challenges_path = os.path.join(config.server_dir, "challenges.json")
        challenges_folder = "challenges"
        other_mode = "solo"
        other_path = os.path.join(config.server_dir, "challenges_solo.json")

    print(f"📖 Loading {mode.upper()} challenges from {challenges_path}")

    try:
        challenge_list = ChallengeList(challenges_file=challenges_path)
        list_type = "Exploration" if mode == "regular" else "Solo"
        user_type = "Admin" if config.base_mode == "admin" else "Student"
        print(f"✅ {user_type} {list_type} Challenge List loaded ({challenge_list.numOfChallenges} challenges).")
        return challenge_list, challenges_folder
    except (FileNotFoundError, json.JSONDecodeError) as err:
        print(f"⚠️ {err.__class__.__name__}: {err}")
        # Try the other mode if its folder is present
        if other_mode in config.AVAILABLE_MODES and os.path.exists(other_path):
            print(f"↪️ Falling back to {other_mode.upper()} due to missing/invalid JSON.")
            return load_challenges(other_mode)
        # Final fail
        raise