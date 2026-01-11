# 🧠 Hex Flag Hunter

**Mission Briefing:**
Hackers left behind a suspicious binary file: `hex_flag.bin`.
It is too small to be a real program, but it contains hidden data.

## 🧠 Intelligence Report
* **The Concept:** Files are just sequences of bytes. Even inside compiled code ("binary noise"), text strings are often stored in plain text.
* **The Strategy:** **Static Analysis**. Instead of running the file (which might be dangerous), we will inspect its raw data.
* **The Warning:** The file contains **multiple candidate flags**, but only one is valid. Check the surrounding data bytes for context.
* **The Tools:**
    * `xxd` – A Hex Dumper that shows the raw data layout.
    * `strings` – A utility that extracts readable text sequences from binary files.

**Your Goal:** Scan the binary, sift through the noise, and find the true flag embedded inside.

## 📂 Files in this folder
* `hex_flag.bin` – The suspicious binary file.

---
**🏁 Flag format:** `CCRI-AAAA-1111`