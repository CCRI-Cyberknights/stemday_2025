# 🖥️ Process Inspection

**Mission Briefing:**
Operatives have planted a rogue process on the system to exfiltrate data.
You have obtained a snapshot (`ps_dump.txt`) of the system’s running processes at the time of the incident.

## 🧠 Intelligence Report
* **The Concept:** Every program running on a computer is a "process." Processes often accept **Command Line Arguments** (flags) when they start.
* **The Clue:** Malware often gives itself away via these arguments (e.g., passing a secret password or flag explicitly in the command).
* **The Strategy:** **Process Auditing**. You must filter through the snapshot to identify any suspicious command-line strings.

**Your Goal:** Analyze the process list, check the command arguments, and identify the process carrying the agency flag.

## 📂 Files in this folder
* `ps_dump.txt` – A snapshot of running processes and their arguments.

---
**🏁 Flag format:** `CCRI-AAAA-1111`