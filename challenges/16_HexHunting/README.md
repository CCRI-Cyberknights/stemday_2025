# 🧠 Hex Flag Hunter

Hackers left behind a suspicious binary file: `hex_flag.bin`.
It is too small to be a real program, but it contains hidden data.

**The Concept:**
Files are just sequences of bytes. Tools like **Hex Editors** allow you to see the raw data (hexadecimal) alongside its ASCII representation. Even inside compiled code, text strings are often visible.

**Your Mission:** Analyze the binary.
1.  Use tools like `strings` to perform a quick scan for readable text.
2.  Use `xxd` or a hex editor to inspect the raw data layout.
3.  Find the flag embedded among the binary noise.

## 📂 Files in this folder
* `hex_flag.bin` – The suspicious binary file.

---
**🏁 Flag format:** `CCRI-AAAA-1111`