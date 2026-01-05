# 🗃️ Challenge 11: Hidden File Hunt

**Mission Briefing:**
A rogue CryptKeeper operative has stashed the agency flag somewhere deep inside the `junk/` directory.
To the naked eye, this folder looks like a boring collection of backups and logs. However, intelligence indicates that the flag is hidden inside a file that "doesn't want to be found."

## 🧠 Intelligence Report
* **The Concept:** **Hidden Files**. In Linux, any file starting with a dot (`.secret`) is hidden from standard directory listings. 
* **The Challenge:** **Recursion**. The folder contains subfolders, which contain more subfolders. You cannot check them one by one.
* **The Trap:** The operative planted **four fake flags** (decoys) to slow you down.

## 📝 Investigator’s Journal
*Notes from the field:*

> "It's a needle in a haystack. I tried running `ls`, but I saw nothing useful.
>
> You need to dig deeper. The flag might be inside a hidden file (a 'dotfile') or buried three levels down in a subdirectory. Don't trust the decoys—if you see a flag like `FLAG-HIDE-1234` or `FAKE-1111`, ignore it. The real one matches our standard format perfectly."

## 📂 Files in This Folder
* `junk/` — A maze of subdirectories containing junk files and the flag.

---

## 🛠 Tools & Techniques

You need tools that can see the invisible and look through walls (folders).

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **ls -a** | Lists **all** files, revealing hidden dotfiles. | `ls -a junk/` |
| **find** | The ultimate search tool. Lists every file in every subfolder recursively. | `find junk/ -type f` |
| **grep -r** | recursively searches the *contents* of files for a pattern. | `grep -r "CCRI-" junk/` |

> 💡 **Tip:** The `find` command is powerful.
> * `-type f` means "look for files only" (ignore folders).
> * `-name ".*"` would find only hidden files.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Recursively search the directory, find the hidden file, and verify the flag format.