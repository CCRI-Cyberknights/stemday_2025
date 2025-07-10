🔓 Hashcat ChainCrack
----------------------

You’ve intercepted 3 encrypted archive segments — each one locked behind a password. Alongside them, you found:  

- `hashes.txt` – A list of MD5 hashes hiding the passwords.  
- `wordlist.txt` – Likely password candidates.  

Your task is to crack the hashes, extract the segments, decode them, and assemble the final flag.  

🧠 **Your mission:**  
1. Run the helper script: `run_chain_crack.sh`  
2. The script will:  
   • Use **Hashcat** to crack all 3 hashes using the provided wordlist.  
   • Unlock each ZIP segment with its cracked password.  
   • Decode the base64-encoded data in each segment.  
   • Reassemble all decoded parts into **5 possible flags**.  

Only **one** of the 5 matches the official format: `CCRI-AAAA-1111`  

📂 **Files in this folder:**  
- `hashes.txt` – 3 MD5 hashes to crack  
- `wordlist.txt` – Possible passwords  
- `segments/` – Folder with 3 encrypted ZIP files  
- `run_chain_crack.sh` – Your interactive cracking assistant  

💡 **Tip:** Watch how each successful crack gets you closer to the goal. Cracking alone doesn’t solve the case — decoding and assembling are just as critical!  

🏁 **Flag format:** CCRI-AAAA-1111

