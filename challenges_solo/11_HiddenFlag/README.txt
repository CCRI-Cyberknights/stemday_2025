# 🕵️ Challenge 11: Hidden File Hunt

A rogue operative may have stashed the real agency flag somewhere deep in this folder structure.

The directory tree you're exploring — named `junk/` — looks like a boring collection of backups and logs… but somewhere inside, a hidden file contains the flag you're after.

Just one problem: four fake flags have also been planted to throw you off the trail.

---

## 🎯 Your Mission

Explore every corner of the `junk/` folder. Some files are easy to find. Others? Not so much.

✅ Only one flag follows the official agency format:  
**CCRI-AAAA-1111**  

❌ Fake flags will use misleading formats like:  
- `FLAG-HIDE-####`  
- `HIDE-####-CODE`  
- `CCRI-1111-FAKE`  
…don’t fall for them.

---

## 🛠 Helpful Tools

These commands will help you uncover hidden files and examine their contents:

| Tool/Command           | What it does                                      |
|------------------------|---------------------------------------------------|
| `ls -a`                | Lists files, including hidden ones (dotfiles)     |
| `find junk/ -type f`   | Lists all files under `junk/`, including hidden   |
| `grep -R CCRI junk/`   | Recursively search for real-looking flags         |
| `cat`                  | Outputs the content of a file                     |
| `file`                 | Tells you what kind of file you’re looking at     |

> 💡 Pro tip: Some files are hidden *and* buried in subdirectories. You’ll need to dig deep.

---

## 📝 Instructions

1. Begin your search in the `junk/` folder.  
2. Use the tools above to recursively explore all files — especially those starting with a dot (`.`).  
3. If you spot a flag, make sure it matches the official format exactly.

Once you’re confident you’ve found the **real** flag, save it like this:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

---

## 📂 Provided Folder

* `junk/` – A maze of subdirectories containing junk files and (possibly) a flag.

---

## 🏁 Flag Format

You’re looking for this exact format:

**CCRI-AAAA-1111**

All other variants are decoys.

---

🧠 Not all files want to be found. Dig with purpose, filter with precision, and don’t be fooled by fakes.
