# 🔓 Hashcat ChainCrack

**Mission Briefing:**
You have intercepted **3 encrypted archive segments** from a data exfiltration attempt. Each segment is locked with a different password.

However, we also found a file (`hashes.txt`) containing the **MD5 hashes** of those passwords.

## 🧠 Intelligence Report
* **The Lock:** Three separate ZIP files (`part1.zip`, `part2.zip`, `part3.zip`).
* **The Keys:** The passwords are hidden behind MD5 hashes. You must crack them to open the archives.
* **The Warning:** Once reassembled, the data will yield **multiple potential flags**. Only one is valid.
* **The Strategy:**
    1.  **Crack:** Use **Hashcat** and the provided `wordlist.txt` to reverse the hashes.
    2.  **Unlock:** Use the revealed passwords to extract the segments.
    3.  **Assemble:** The extracted files are fragments. You must combine them to reconstruct the final flag list.

**Your Goal:** Execute the crack, unlock the segments, and reassemble the intelligence.

## 📂 Files in this folder
* `hashes.txt` – The list of target MD5 hashes.
* `wordlist.txt` – A list of candidate passwords.
* `segments/` – A folder containing the encrypted ZIP files.

---
**🏁 Flag format:** `CCRI-AAAA-1111`