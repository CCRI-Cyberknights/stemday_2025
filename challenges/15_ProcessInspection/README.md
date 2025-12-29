# 🖥️ Process Inspection

Operatives have planted a rogue process on the system to exfiltrate data.
You have obtained a snapshot (`ps_dump.txt`) of the system’s running processes at the time of the incident.

**The Concept:**
Every program running on a computer is a "process." Processes often accept **Command Line Arguments** (flags) when they start. Malware often gives itself away via these arguments.

**Your Mission:** Audit the process list.
1.  Analyze the process snapshot.
2.  Look at the command arguments for every running service.
3.  Identify the suspicious process carrying the agency flag.

## 📂 Files in this folder
* `ps_dump.txt` – A snapshot of running processes and their arguments.

---
**🏁 Flag format:** `CCRI-AAAA-1111`