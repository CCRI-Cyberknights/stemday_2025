import json
import os
from Challenge import Challenge

class ChallengeList:
    """
    Class to manage a list of challenges.

    Attributes:
        challenges (list): A list of Challenge objects.
        completed_challenges (list): A list of completed challenges.
        numOfChallenges (int): Total number of challenges.
    """

    def __init__(self, challenges_file: str = "challenges.json"):
        """
        Initializes the ChallengeList by loading challenges from a JSON file.
        Resolves JSON relative to web_version folder.
        """
        self.challenges = []
        self.completed_challenges = []
        self.numOfChallenges = 0

        # === Resolve path to JSON relative to web_version folder ===
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.challenges_path = os.path.join(base_dir, challenges_file)

        # === Determine if we are in Solo mode ===
        if os.path.basename(self.challenges_path) == "challenges_solo.json":
            self.solo_mode = True
            challenges_folder_name = "challenges_solo"
        else:
            self.solo_mode = False
            challenges_folder_name = "challenges"

        # === Set parent challenges folder ===
        self.challenges_root = os.path.normpath(
            os.path.join(base_dir, "..", challenges_folder_name)
        )

        print(f"📖 Checking for challenges file at: {self.challenges_path}")
        self.load_challenges()

    def load_challenges(self):
        """Loads challenges from a JSON file and populates the Challenge list."""
        if not os.path.exists(self.challenges_path):
            print(f"❌ ERROR: Challenges file not found at {self.challenges_path}")
            return

        try:
            with open(self.challenges_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ ERROR: Invalid JSON in {self.challenges_path}: {e}")
            return

        print(f"✅ Loaded {len(data)} challenges from {self.challenges_path}")
        order = 1
        for key, entry in data.items():
            challenge = Challenge(
                id=key,
                ch_number=order,
                name=entry['name'],
                folder=entry['folder'],
                flag=entry['flag'],
                script=entry.get('script'),  # May not exist in Solo JSON
                solo_mode=self.solo_mode
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
        Ensures script paths are saved relative to their folder.
        """
        try:
            data = {}
            for c in self.challenges:
                folder_name = os.path.basename(c.getFolder())  # Just the folder name
                entry = {
                    "name": c.getName(),
                    "folder": folder_name,
                    "flag": c.getFlag()
                }
                if not self.solo_mode and c.getScript():
                    # Only include script in Guided mode
                    script_name = os.path.basename(c.getScript())
                    entry["script"] = script_name

                data[c.getId()] = entry

            with open(self.challenges_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Saved updated challenges to {self.challenges_path}")
        except Exception as e:
            print(f"❌ ERROR: Failed to save challenges: {e}")
            raise
