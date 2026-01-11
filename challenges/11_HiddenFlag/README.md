# 🕵️ Hidden File Hunt

**Mission Briefing:**
The flag is hidden somewhere inside the `junk/` directory.
However, the directory is a maze filled with decoy folders, fake archives, and system backups.

## 🧠 Intelligence Report
* **The Environment:** A complex folder structure (`junk/`) with many subdirectories.
* **The Camouflage:** The target file might be a **Hidden File** (a filename starting with a `.`, which makes it invisible to standard `ls` commands).
* **The Strategy:** **Recursive Search**. Instead of opening folders one by one, we will use a tool that digs through the entire tree automatically.
* **The Tool:** `grep -r` allows us to search for specific text inside every file in a directory structure simultaneously.
* **The Warning:** Beware of **decoy files** containing fake flags.

**Your Goal:** Use recursive tools to locate the file containing the valid flag, then read it.

## 📂 Files in this folder
* `junk/` – A messy directory structure containing the hidden flag.

---
**🏁 Flag format:** `CCRI-AAAA-1111`