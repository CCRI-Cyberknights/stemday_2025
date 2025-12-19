import os
import base64
import config  # Now imports path logic from your new config module

class Challenge:
    """Represents a single CTF challenge."""

    def __init__(self, id, ch_number, name, folder, flag, script=None, solo_mode=False):
        self.id = id                      # Unique identifier
        self.ch_number = ch_number        # Challenge number for display
        self.name = name                  # Human-readable name
        self.complete = False             # Default: not completed

        # === Determine base path via Config ===
        # We rely on config.py to tell us where the SOLO and REGULAR (Guided) folders are.
        challenges_root = config.SOLO_DIR if solo_mode else config.GUIDED_DIR
        
        # Normalize the full path
        self.folder = os.path.normpath(os.path.join(challenges_root, folder))

        # Scripts are only in Guided mode
        self.script = (
            os.path.normpath(os.path.join(self.folder, script)) if script else None
        )

        # === Student/Admin mode determines flag decoding ===
        # We check the environment variable directly to allow runtime switching if needed,
        # although config.base_mode generally mirrors this.
        mode = os.environ.get("CCRI_CTF_MODE", "student").lower()
        self.flag = self.decode_flag(flag) if mode == "student" else flag

    def decode_flag(self, encoded_flag: str) -> str:
        """Decode XOR+Base64 encoded flag using the student key."""
        key = "CTF4EVER"
        try:
            raw = base64.b64decode(encoded_flag)
            return "".join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(raw))
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
            f"Folder={self.folder} | Script={self.script} | Flag={self.flag}"
        )