# 🗃️ Challenge 11: Hidden File Hunt

A rogue operative may have stashed the real agency flag somewhere deep in this folder structure.

The directory tree you’re exploring — `junk/` — looks like a boring collection of backups and logs… but somewhere inside, a hidden file contains the flag you’re after.

Just one problem: **four fake flags** have also been planted to throw you off the trail.

Some files are easy to find. Others? Not so much.
Not all files *want* to be found.

Dig with purpose, filter with precision, and don’t be fooled by fakes.

Only one true flag follows the official knight format:

**`CCRI-AAAA-1111`**

Fake flags may appear using misleading formats such as:

* `FLAG-HIDE-####`
* `HIDE-####-CODE`
* `CCRI-1111-FAKE`

…don’t fall for them.

---

## 🛠 Tools & Techniques

| Tool / Command       | What It Does                                   |
| -------------------- | ---------------------------------------------- |
| `ls -a`              | Lists files — including hidden dotfiles        |
| `find junk/ -type f` | Lists **all** files under `junk/`, recursively |
| `grep -R CCRI junk/` | Searches for real-looking flags recursively    |
| `cat`                | Outputs file contents                          |
| `file`               | Identifies file type                           |

> 🔎 **Pro Tip:** Some files are hidden *and* buried in subdirectories. You’ll need to dig deep.

---

## 📝 Objective

1. Begin your search in the `junk/` folder.
2. Use the tools above to recursively explore all files — especially those starting with a dot (`.`).
3. If you spot a flag, verify that it matches the official format **exactly**.
4. Ignore fakes and locate the real `CCRI-AAAA-1111` flag.

---

## 📂 Files in This Folder

* `junk/` — A maze of subdirectories containing junk files and (possibly) a flag.

---

## 🏁 Flag Format

All flags follow this structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then input the flag into the website to verify the answer.