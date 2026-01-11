# 📜 Log Analysis Challenge

**Mission Briefing:**
A server has been compromised. The system administrators have provided the `auth.log` file, which records every login attempt.

The file contains thousands of lines of noise. Somewhere in there, a hacker successfully logged in or executed a suspicious command.

## 🧠 Intelligence Report
* **The Problem:** The log file is too large to read line-by-line.
* **The Needle:** We are looking for the agency flag format (`CCRI-...`) or suspicious pattern matches.
* **The Strategy:** **Filtering**. Instead of reading everything, we display only the lines that match our criteria.
* **The Tool:** `grep` (Global Regular Expression Print) is the standard Linux tool for searching plain-text data sets.
* **The Warning:** The log contains **decoy entries** designed to mislead investigators.

**Your Goal:** Filter the noise to identify the specific log entry that contains the valid flag.

## 📂 Files in this folder
* `auth.log` – A large server log file containing thousands of entries.

---
**🏁 Flag format:** `CCRI-AAAA-1111`