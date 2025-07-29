import os
import base64

class Challenge:
    """Represents a single CTF challenge."""

    def __init__(self, id, ch_number, name, folder, flag, script=None, solo_mode=False):
        self.id = id  # Unique identifier
        self.ch_number = ch_number  # Challenge number for display
        self.name = name  # Human-readable name
        self.complete = False  # Default: not completed

        # Determine base path for challenges
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if solo_mode:
            challenges_dir = os.path.join(base_dir, "challenges_solo")
        else:
            challenges_dir = os.path.join(base_dir, "challenges")

        self.folder = os.path.normpath(os.path.join(challenges_dir, folder))

        # Scripts are only in Guided mode
        if script:
            self.script = os.path.normpath(os.path.join(self.folder, script))
        else:
            self.script = None

        # Determine if we're in student or admin mode
        mode = os.environ.get("CCRI_CTF_MODE", "student").lower()

        if mode == "student":
            self.flag = self.decode_flag(flag)
        else:
            self.flag = flag

    def decode_flag(self, encoded_flag):
        """Decode XOR+Base64 encoded flag using the student key."""
        key = "CTF4EVER"
        try:
            raw = base64.b64decode(encoded_flag)
            return ''.join([chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(raw)])
        except Exception as e:
            print(f"❌ ERROR decoding student flag: {e}")
            return "[INVALID FLAG]"

    def setComplete(self):
        self.complete = True

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getFolder(self):
        return self.folder

    def getScript(self):
        return self.script

    def getFlag(self):
        return self.flag

    def __repr__(self):
        return (
            f"#{self.ch_number} {self.name} | ID={self.id} | "
            f"Folder={self.folder} | Script={self.script} | "
            f"Flag={self.flag}"
        )
