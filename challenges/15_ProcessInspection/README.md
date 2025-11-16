🖥️ Challenge 15: Process Inspection
====================================

CryptKeeper operatives have planted a rogue process on a compromised system to exfiltrate sensitive data.  
You’ve obtained a snapshot of the system’s running processes. Hidden within the **command-line arguments** of five suspicious processes are “flags” — but only ONE of them is authentic. The rest are decoys.  

🎯 **Your Mission:**  
1. Investigate each process in the snapshot.  
2. Examine their command-line arguments for embedded flags.  
3. Identify which one matches the official agency flag format.  

🗂️ **Files in this folder:**  
• ps_dump.txt – Snapshot of running processes  
• explore_processes.sh – Interactive helper script  

💡 **Hint:**  
The real flag follows the agency format:  
   `CCRI-AAAA-1111`  
Fake flags use other prefixes or slightly altered structures.  

👩‍💻 **Tip:** Use the guided helper script to filter, search, and explore process details.  
It will highlight arguments and save interesting results for later review.  

---

🚀 *Start your investigation and uncover the rogue process now!*

