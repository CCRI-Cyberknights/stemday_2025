import os
class Challenge:
    complete = False  # Default to not completed

    def __init__(self, id, ch_number, name, folder, script, flag, key):
        self.name = name
        self.ch_number = ch_number
        folder_dir = os.path.dirname(os.path.abspath(__file__).replace("/web_version_admin/utils/", "/challenges/"))
        self.folder = os.path.join(folder_dir, folder)  # To remove '../' from the folder path add [2:] to 'folder' in the join function
        self.script = os.path.join(self.folder, script)
        self.flag = flag
        self.key = key
        self.id = id  # Unique identifier for the challenge

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
    
    def getKey(self):
        return self.key

    def __repr__(self):
        return f"#{self.ch_number}, {self.name} -> ID={self.id}, FOLDER={self.folder}, SCRIPT={self.script}, FLAG={self.flag}, KEY={self.key}"