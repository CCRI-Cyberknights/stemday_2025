import os

class Challenge:
    """Represents a single CTF challenge."""

    def __init__(self, id, ch_number, name, folder, script, flag):
        self.id = id  # Unique identifier
        self.ch_number = ch_number  # Challenge number for display
        self.name = name  # Human-readable name
        self.complete = False  # Default: not completed
        self.flag = flag  # Real flag (plaintext in admin version)

        # === Resolve challenge folder path ===
        # BASE_DIR is the parent directory where web_version and challenges folders live
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        challenges_dir = os.path.join(base_dir, "challenges")
        self.folder = os.path.normpath(os.path.join(challenges_dir, folder))
        self.script = os.path.normpath(os.path.join(self.folder, script))

    def setComplete(self):
        """Mark this challenge as completed."""
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
