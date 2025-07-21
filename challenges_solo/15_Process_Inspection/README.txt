# 🖥️ Challenge 15: Process Inspection

Liber8 operatives have planted a rogue process on a compromised system to exfiltrate sensitive data.  
You’ve obtained a snapshot of the system’s running processes. Hidden within the command-line arguments of five suspicious processes are “flags” — but only ONE of them is authentic. The rest are decoys.

---

## 🎯 Your Mission

1. Investigate each process in the snapshot.  
2. Examine their command-line arguments for embedded flags.  
3. Identify which one matches the official agency flag format.

---

## 🛠 Tools You Might Use

- less – View and scroll through the process snapshot.  
- grep – Search for flag-like patterns in the file (e.g., `grep "CCRI-" ps_dump.txt`).  
- awk/cut – Extract specific fields like command-line arguments for review.  

---

## 📝 Challenge Instructions

1. Open ps_dump.txt and review the running processes carefully.  
2. Focus on command-line arguments — look for flag-like strings hidden there.  
3. Remember: only one flag matches the agency’s official format. Decoys may use fake prefixes or slightly altered structures.  

Note: If you find the correct flag, save it manually:

echo "CCRI-AAAA-1111" > flag.txt

---

## 🗂️ Files in this folder

- ps_dump.txt – Snapshot of running processes.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge is about thinking like a systems analyst and learning how to spot suspicious patterns in process data.
