# 🔓 Hashcat ChainCrack

You have intercepted **3 encrypted archive segments**. Each segment is locked, but we found a list of **MD5 hashes** (`hashes.txt`) that correspond to the passwords.

To solve this, you must chain together several techniques:
1.  **Crack:** Use the provided tools (like Hashcat) and the `wordlist.txt` to reverse the hashes and reveal the passwords.
2.  **Unlock:** Use those passwords to open the ZIP segments.
3.  **Assemble:** Combine the data found in the segments to reveal the final flag.

## 📂 Files in this folder
* `hashes.txt` – 3 MD5 hashes hiding the passwords.
* `wordlist.txt` – A list of candidate passwords.
* `segments/` – A folder containing the encrypted ZIP files.

---
**🏁 Flag format:** `CCRI-AAAA-1111`