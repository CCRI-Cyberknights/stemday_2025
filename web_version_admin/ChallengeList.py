import json
import os
from Challenge import Challenge

class ChallengeList:
    """Class to manage a list of challenges.
    
    Attributes:
        challenges (list): A list of Challenge objects.
        completed_challenges (list): A list of completed challenges.
        numOfChallenges (int): Total number of challenges.

    Methods:
        __init__: Initializes the ChallengeList by loading challenges from a JSON file.
        load_challenges: Loads challenges from a JSON file and returns a list of Challenge objects.
        get_challenges: Returns the list of challenges.
        get_challenge_by_id: Returns a challenge object by its ID.
        get_list_of_ids: Returns a list of challenge IDs.
    """

    challenges = []
    '''List of challenges managed by the ChallengeList class.'''
    completed_challenges = []
    '''List of completed challenges.'''
    numOfChallenges = 0
    '''Total number of challenges.'''

    def __init__(self):
        """Initializes the ChallengeList by loading challenges from a JSON file."""
        self.challenges = self.load_challenges()
        print (f"ChallengeList initialized with {len(self.challenges)} challenges.")
        for challenge in self.challenges:
            print(f"Loaded challenge: {challenge.__repr__()}")
        self.numOfChallenges = len(self.challenges)

    def load_challenges(self) -> list[Challenge]:
        """Loads challenges from a JSON file and returns a list of Challenge objects."""
        current_dir = os.path.dirname(os.path.abspath(__file__).replace("utils", ""))
        # print(f"Current directory: {current_dir}")

        challenges_path = os.path.join(current_dir, 'challenges.json')
        print(f"Checking for challenges file at: {challenges_path}")

        if not os.path.exists(challenges_path):
            print(f"Challenges file not found at {challenges_path}.")
            return []

        with open(challenges_path, 'r') as f:
            try:
                data = json.load(f)
                print(f"Loaded {len(data)} challenges from {challenges_path}")
                # print("Challenges:", data)
                print("Storing challenges in ChallengeList...")
                challenges = []
                order = 1
                for key in data.keys():
                    new_challenge = Challenge(
                        id=key,
                        ch_number=order,
                        name=data[key]['name'],
                        folder=data[key]['folder'],
                        script=data[key]['script'],
                        flag=data[key]['flag'],
                        key=data[key]['key']
                    )
                    print(f"Creating Challenge object: {new_challenge.__repr__()}")
                    challenges.append(new_challenge)
                    order += 1

                return challenges

            except json.JSONDecodeError:
                print("Error decoding JSON from challenges file.")
                return []
            
    def get_challenges(self) -> list[Challenge]:
        """Returns the list of challenges."""
        return self.challenges
    
    def get_challenge_by_id(self, challenge_id) -> Challenge | None:
        """Returns a challenge object by its ID.
        
        This function iterates through the list of challenges
        and returns the first challenge that matches the given ID.

        Args:
            challenge_id (str): The ID of the challenge to retrieve.

        Returns:
            Challenge (Challenge | None): The challenge object if found, otherwise None.
        
        """
        for challenge in self.challenges:
            if challenge.getId() == challenge_id:
                return challenge
        return None
    
    def get_list_of_ids(self) -> list[str]:
        """Returns a list of challenge IDs."""
        return [challenge.getId() for challenge in self.challenges]