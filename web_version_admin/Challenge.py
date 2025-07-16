import os

class Challenge:
    """Represents a single CTF challenge."""
    
    def __init__(self, id, ch_number, name, folder, script, flag, key):
        self.id = id  # Unique identifier
        self.ch_number = ch_number  # Challenge number for display
        self.name = name  # Human-readable name
        self.complete = False  # Default: not completed
        self.key = key  # XOR/obfuscation key
        self.flag = flag  # Real flag (base64+XOR encoded in student version)

        # Normalize paths for consistency
        root_dir = os.path.dirname(
            os.path.abspath(__file__).replace(
                "/web_version_admin/utils", "/challenges"
            )
        )
        self.folder = os.path.normpath(os.path.join(root_dir, folder))
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

    def getKey(self):
        return self.key

    def __repr__(self):
        return (
            f"#{self.ch_number} {self.name} | ID={self.id} | "
            f"Folder={self.folder} | Script={self.script} | "
            f"Flag={self.flag} | Key={self.key}"
        )
