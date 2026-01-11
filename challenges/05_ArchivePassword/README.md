# 🔐 ZIP File Crack & Decode

**Mission Briefing:**
You have recovered a mysterious ZIP archive: `secret.zip`. It is password-protected, and standard extraction methods fail without the key.

However, during the data recovery, we also found a `wordlist.txt` file containing thousands of potential passwords.

## 🧠 Intelligence Report
* **The Lock:** Standard ZIP encryption.
* **The Strategy:** **Dictionary Attack**. This involves automating the process of trying every single word in a list until one works.
* **The Requirement:** You cannot do this by hand. You must use (or build) an automated tool to try the passwords rapidly.
* **The Warning:** The recovered file contains **multiple flag candidates**. You must determine which one is the real flag.

**Your Goal:** Execute a dictionary attack to crack the password, extract the archive, and decode the flag inside.

## 📂 Files in this folder
* `secret.zip` – The password-protected archive.
* `wordlist.txt` – A list of common passwords to attempt.

---
**🏁 Flag format:** `CCRI-AAAA-1111`