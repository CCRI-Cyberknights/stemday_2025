# 🕵️ Challenge 08: Fake Auth Log Investigation

You’ve recovered a suspicious system log: auth.log.

It’s packed with fake SSH login records — but buried in the noise is one hidden flag.

---

## 🧠 What’s Going On?

System logs like auth.log record login attempts and system authentication events. Attackers sometimes hide data in logs, hoping it will blend in with normal activity. 

In this case, some entries have odd-looking process IDs (PIDs) that don’t follow normal number patterns. Only one of these anomalies contains the valid flag.

---

## 🛠 Tools You Might Use

- grep – Scan for keywords or patterns in large log files.  
- less – View and scroll through logs efficiently.  
- awk – Extract specific fields from log entries.  
- head/tail – Quickly view the beginning or end of a file.  

---

## 📝 Challenge Instructions

1. Open auth.log and scan through the login entries.  
2. Look for PIDs that seem unusual or don’t match typical numeric patterns.  
3. Use grep and other tools to isolate suspicious entries.  
4. Search for any flag-like strings in the output.  

Hint: Not every strange PID hides a flag. Only one matches the official agency format.

Note: If you spot the correct flag on screen, save it yourself:

echo "CCRI-AAAA-1111" > flag.txt

---

## 📂 Files in this folder

- auth.log – Fake system log to investigate.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge is about analyzing log files like a system administrator to detect hidden anomalies.
