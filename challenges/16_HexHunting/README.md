🧠 Challenge 16: Hex Flag Hunter
=================================

CryptKeeper hackers left behind a suspicious binary file: `hex_flag.bin`.  
It’s too small to be a real program, but something about it feels… hidden.  

🎯 **Your Mission:**  
Analyze the binary and uncover the **real agency flag** embedded in its data.  

📖 **Hints:**  
- The flag is hidden as ASCII text within the binary.  
- It follows this format: `CCRI-AAAA-1111`  
- There are **five candidate flags** in the file — but only ONE is correct.  
- Look for patterns carefully: some decoys are designed to mislead you.  

🛠️ **Tools at Your Disposal:**  
• `strings` → Extracts readable text from binaries (quick scan).  
• `xxd` → Displays hex and ASCII side-by-side for deeper inspection.  
• `hexedit` → Opens the binary in an interactive hex editor for scrolling/searching.  

📂 **Files Provided:**  
• `hex_flag.bin` – Suspicious binary to investigate  
• `inspect_binary.sh` – Interactive helper script to guide you  

---

🚩 **Goal:** Find and submit the one valid flag in the format:  
`CCRI-AAAA-1111`

