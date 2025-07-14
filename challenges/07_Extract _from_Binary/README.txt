# 🔍 Extract from Binary

A mysterious binary file has appeared: hidden_flag.

Your mission is to perform a forensic analysis of the file and recover the real agency flag.

Only one of the embedded strings matches the official format: CCRI-AAAA-1111

---

## 🧠 What’s Going On?

Binary files often contain hidden or human-readable data mixed with raw machine instructions. Forensic analysts use specialized tools to scan binaries and extract meaningful information.

This challenge is about finding those pieces of information and identifying the real flag.

---

## 🛠 Tools You Might Use

- strings – Extracts human-readable text from binary files.  
- hexdump – Displays the binary data in a readable hexadecimal and ASCII format.  
- grep – Searches through extracted text for patterns like “CCRI-”.  

---

## 📝 Challenge Instructions

1. Examine hidden_flag. Consider its size and type.  
2. Use strings or a hex viewer to scan the binary for embedded text.  
3. Search for any candidate flags in the output.  

Hint: There may be multiple flag-like patterns. Only one fits the official format.

Note: If you find the correct flag on screen, save it manually:

echo "CCRI-AAAA-1111" > flag.txt

---

## 📂 Files in this folder

- hidden_flag – The binary containing hidden data.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge is about using forensic tools to pull hidden clues from compiled files.
