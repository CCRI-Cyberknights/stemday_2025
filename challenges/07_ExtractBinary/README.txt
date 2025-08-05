🔍 Extract from Binary
=======================

A mysterious binary file has appeared: `hidden_flag`.  

Your mission is to perform a forensic analysis of the file and recover the **real agency flag**.  

Only **one** of the embedded strings matches the official format: `CCRI-AAAA-1111`  

🛠️ **Tools You’ll Use:**  
- `strings` – Extracts human-readable text from binary files.  

🧠 **Your steps:**  
1. Run the interactive helper: `analyze_binary.sh`  
2. The script will extract all text from the binary and save it for review.  
3. Inspect the extracted data and look for flag-like patterns.  

📂 **Files in this folder:**  
- `hidden_flag` → The binary containing hidden data  
- `analyze_binary.sh` → Your guided forensic assistant  

💡 **Tip:** Pay attention to patterns and don’t assume the first candidate is correct.  

🏁 **Flag format:** CCRI-AAAA-1111

