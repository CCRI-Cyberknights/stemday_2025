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
        Optionally accepts a custom path to challenges.json.
        """
        self.challenges = []
        self.completed_challenges = []
        self.numOfChallenges = 0
        
        # Resolve path to JSON
        base_dir = os.path.dirname(os.path.abspath(__file__).replace("utils", ""))
        self.challenges_path = os.path.join(base_dir, challenges_file)

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
                folder=os.path.normpath(entry['folder']),
                script=entry['script'],
                flag=entry['flag'],
                key=entry['key']
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
