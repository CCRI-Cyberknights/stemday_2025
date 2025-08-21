import json
import os
import re
from Challenge import Challenge

# When running from the .pyz, __main__ sets this to the on-disk web_version path
ASSETS_DIR_OVERRIDE = os.environ.get("CCRI_ASSETS_DIR")


class ChallengeList:
    """
    Manages a list of challenges loaded from a JSON mapping:
      {
        "01_Stego": {
          "name": "...",
          "folder": "01_Stego",
          "flag": "...",          # encoded in student builds; plaintext in admin
          "script": "helper.py"   # optional; guided only
        },
        ...
      }
    """

    _num_prefix = re.compile(r"^(\d+)")

    def __init__(self, challenges_file: str = "challenges.json"):
        """
        Initializes the ChallengeList by loading challenges from a JSON file.
        Supports absolute or relative paths (relative resolved under assets dir).
        """
        self.challenges = []
        self.completed_challenges = []
        self.numOfChallenges = 0
        self._encoded_flags = {}  # id -> encoded flag exactly as read from JSON

        # === Where JSON/templates/static live ===
        assets_dir = (
            os.path.abspath(ASSETS_DIR_OVERRIDE)
            if ASSETS_DIR_OVERRIDE
            else os.path.dirname(os.path.abspath(__file__))
        )

        # Absolute paths stay absolute; relative resolves under assets_dir
        self.challenges_path = (
            challenges_file
            if os.path.isabs(challenges_file)
            else os.path.join(assets_dir, challenges_file)
        )

        # === Determine Solo vs Guided based on filename ===
        if os.path.basename(self.challenges_path) == "challenges_solo.json":
            self.solo_mode = True
            challenges_folder_name = "challenges_solo"
        else:
            self.solo_mode = False
            challenges_folder_name = "challenges"

        # === Environment mode (student/admin) for persistence behavior ===
        self.mode = os.environ.get("CCRI_CTF_MODE", "student").lower()
        print(f"🔍 Environment mode detected: {self.mode}")

        # === Where the real challenge folders live ===
        # parent of the assets dir (project root): .../(challenges|challenges_solo)
        project_root = os.path.abspath(os.path.join(assets_dir, ".."))
        self.challenges_root = os.path.normpath(
            os.path.join(project_root, challenges_folder_name)
        )

        print(f"📖 Checking for challenges file at: {self.challenges_path}")
        self.load_challenges()

    # -------- Helpers --------

    @staticmethod
    def _natural_key(ch_id: str):
        """
        Sort key that tries to respect numeric prefixes like '01_', '12_', etc.
        Falls back to lowercase alphabetical if no leading number.
        """
        m = ChallengeList._num_prefix.match(ch_id)
        if m:
            try:
                return (0, int(m.group(1)), ch_id.lower())
            except ValueError:
                pass
        return (1, ch_id.lower())

    # -------- Loading / Saving --------

    def load_challenges(self):
        """Loads challenges, validates schema, and populates the list.

        Raises:
            FileNotFoundError: if JSON file missing.
            json.JSONDecodeError: if JSON invalid or schema issues detected.
        """
        if not os.path.exists(self.challenges_path):
            raise FileNotFoundError(self.challenges_path)

        try:
            with open(self.challenges_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise

        # Expect a mapping id -> entry
        if not isinstance(data, dict):
            raise json.JSONDecodeError(
                "Top-level JSON must be an object (mapping of id->entry).", "", 0
            )

        print(f"✅ Loaded {len(data)} challenges from {self.challenges_path}")

        order = 1
        # Stable/natural-ish order by challenge id
        for key in sorted(data.keys(), key=self._natural_key):
            entry = data[key]

            # Validate required fields; surface as JSON errors
            for req in ("name", "folder", "flag"):
                if req not in entry:
                    raise json.JSONDecodeError(
                        f"Missing required field '{req}' in challenge '{key}'.", "", 0
                    )

            # Remember the encoded flag exactly as it appears in file
            self._encoded_flags[key] = entry["flag"]

            challenge = Challenge(
                id=key,
                ch_number=order,
                name=entry["name"],
                folder=entry["folder"],   # Challenge resolves full path itself
                flag=entry["flag"],       # Challenge decodes at runtime in student mode
                script=entry.get("script"),
                solo_mode=self.solo_mode,
            )

            print(f"➡️  Challenge #{order}: {challenge.getName()} (ID={key})")
            self.challenges.append(challenge)
            order += 1

        self.numOfChallenges = len(self.challenges)
        print(f"📦 ChallengeList initialized with {self.numOfChallenges} challenges.")

    def get_challenges(self):
        """Returns the list of Challenge objects."""
        return self.challenges

    def get_challenge_by_id(self, challenge_id):
        """Retrieve a Challenge object by its ID."""
        return next((c for c in self.challenges if c.getId() == challenge_id), None)

    def get_list_of_ids(self):
        """Return a list of all challenge IDs."""
        return [c.getId() for c in self.challenges]

    def save_challenges(self):
        """
        Saves the current challenges (including updated flags) back to the JSON file.
        Ensures script names are saved as basenames.
        In student mode, preserves the originally loaded encoded flags.
        """
        data = {}

        for c in self.challenges:
            folder_name = os.path.basename(c.getFolder())

            # Preserve encoded flag in student mode
            encoded_from_file = self._encoded_flags.get(c.getId())
            flag_to_write = (
                encoded_from_file if (self.mode == "student" and encoded_from_file) else c.getFlag()
            )

            entry = {
                "name": c.getName(),
                "folder": folder_name,
                "flag": flag_to_write,
            }

            # Only persist script for guided (regular) sets, normalize to basename
            if not self.solo_mode and c.getScript():
                entry["script"] = os.path.basename(c.getScript())

            data[c.getId()] = entry

        try:
            with open(self.challenges_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved updated challenges to {self.challenges_path}")
        except Exception as e:
            print(f"❌ ERROR: Failed to save challenges: {e}")
            raise
