📡 Challenge 13: HTTP Headers Mystery
======================================

CryptKeeper operatives have been exchanging secret messages through HTTP servers.  
You’ve intercepted **five HTTP response files**, but only ONE contains the real agency flag. The others are decoys designed to mislead intruders.  

🎯 **Your Mission:**  
1. Investigate each HTTP response carefully.  
2. Look for a hidden `X-Flag:` header in the response.  
3. Identify the correct flag in this format:  
   `CCRI-AAAA-1111`  

🗂️ **Files in this folder:**  
• response_1.txt – Captured HTTP response #1  
• response_2.txt – Captured HTTP response #2  
• response_3.txt – Captured HTTP response #3  
• response_4.txt – Captured HTTP response #4  
• response_5.txt – Captured HTTP response #5  
• explore_responses.sh – Guided helper script  

💡 **Hint:** Only one flag starts with `CCRI-`. All others use fake prefixes.  

👩‍💻 **Tip:**  
Use the helper script to review the responses interactively.  
- Tools like `less`, `grep`, and `cat` are built in.  
- When viewing with `less`, press **q** to return to the menu.  

---

🚀 *Ready to uncover the hidden flag?*

