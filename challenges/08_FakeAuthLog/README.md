# 📜 Log Analysis Challenge

A server has been compromised. The system administrators have provided the `auth.log` file, which records every login attempt.

The file contains thousands of lines of noise. Somewhere in there, a hacker successfully logged in or executed a suspicious command.

**Your Mission:** Filter the noise.
1.  Analyze the log file (`auth.log`).
2.  Use text processing tools (like `grep`) to search for keywords like "Accepted", "root", or the agency flag format.
3.  Identify the specific log entry that contains the flag.

## 📂 Files in this folder
* `auth.log` – A large server log file containing thousands of entries.

---
**🏁 Flag format:** `CCRI-AAAA-1111`