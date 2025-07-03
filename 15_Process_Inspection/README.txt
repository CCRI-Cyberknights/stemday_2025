🖥️ Challenge #15 – Process Inspection
-------------------------------------------

Your mission: Investigate a compromised system and identify the rogue process used by Liber8 to exfiltrate data.

You’ve obtained a snapshot of the running processes on the target system. Five suspicious processes appear to include "flags" in their command-line arguments, but only ONE of these flags is the **real agency flag**—the others are decoys.

🗂️ Files in this folder:
  • ps_dump.txt             ← Snapshot of running processes
  • explore_processes.sh    ← Guided helper script

💡 Hint: The real flag starts with **CCRI-** and uses this format:  
       **CCRI-AAAA-1111**  
The fake flags have different prefixes.

👩‍💻 Tip: Use the helper script to filter and search the process list for possible flags.

🚀 Begin your investigation and identify the rogue process!

