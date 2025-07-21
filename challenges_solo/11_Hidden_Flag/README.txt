# 🧠 Challenge 11: Hidden File Hunt

Somewhere in this folder structure lies a hidden file containing the real agency flag.

But beware — four fake flags have been planted to confuse intruders. Only one follows the official format.

---

## 🎯 Your Mission

Explore the directory tree, uncover hidden files, and locate the *one* valid flag.

✅ Official flag format: CCRI-AAAA-1111  
❌ Fake flags may look similar but use the wrong prefix or order:  
   - FLAG-HIDE-####  
   - HIDE-####-CODE  
   - etc.  

Your goal is to identify and save only the correct flag.

---

## 🛠 Tools You Might Use

- ls -a – List all files, including hidden ones (those starting with a dot).  
- find – Search recursively for hidden files in subdirectories.  
- cat – View the contents of discovered files.  
- grep – Filter for flag-like patterns.  

---

## 📝 Challenge Instructions

1. Explore the junk/ folder and its subdirectories.  
2. Use the tools above to uncover hidden files and check their contents.  
3. Be careful to verify the format of each flag you find.  

Note: If you find the correct flag, save it manually:

echo "CCRI-AAAA-1111" > flag.txt

---

## 📂 Folder to Explore

- junk/ – The directory tree hiding the flag.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge is about exploring the Linux filesystem and thinking like a forensics analyst searching for hidden evidence.
