# 🕵️ Stego Decode Challenge

**Mission Briefing:**
We have recovered a suspicious image file (`squirrel.jpg`) from a target machine. While it looks like a normal picture, our analysts believe it has been altered using **Steganography** — the art of hiding secret data inside ordinary files to avoid detection.

## 🧠 Intelligence Report
* **The Lock:** Steganography tools usually require a **passphrase** to extract the hidden data.
* **The Key:** We believe the user practiced poor security hygiene. The password is rumored to be **"the most common password in the world."**
* **The Tool:** We have deployed `steghide` to this environment to help you attempt the extraction.

**Your Goal:** Guess the password based on the intel, unlock the file, and retrieve the flag.

## 📂 Files in this folder
* `squirrel.jpg` – The suspicious image containing the hidden flag.

---
**🏁 Flag format:** `CCRI-AAAA-1111`