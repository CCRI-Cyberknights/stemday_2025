🕵️ Challenge 08: Fake Auth Log Investigation
==============================================

You’ve recovered a suspicious system log: `auth.log`.  

It’s packed with fake SSH login records — but buried in the noise is **one hidden flag**.  

🔑 The clue? Some entries have **odd-looking process IDs (PIDs)** that don’t follow normal number patterns. Only **one** of these anomalies contains the valid flag.  

🛠️ **Tools You’ll Use:**  
- `grep` – Scan for suspicious entries in system logs.  

🧠 **Your steps:**  
1. Run the interactive helper: `investigate_authlog.sh`  
2. The script will scan `auth.log` and highlight suspicious entries.  
3. Review the findings and search for patterns or keywords.  
4. Identify the **real flag** in the format: `CCRI-AAAA-1111`  

📂 **Files in this folder:**  
- `auth.log` → Fake system log to investigate    

💡 **Tip:** Not every strange PID hides a flag. Look for the **agency’s exact format** and don’t get distracted by decoys.  

