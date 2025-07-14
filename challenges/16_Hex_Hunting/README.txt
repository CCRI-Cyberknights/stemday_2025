# 🧠 Challenge 16: Hex Flag Hunter

Liber8 hackers left behind a suspicious binary file: hex_flag.bin.  
It’s too small to be a real program, but something about it feels… hidden.

---

## 🎯 Your Mission

Analyze the binary and uncover the real agency flag embedded in its data.

---

## 📖 Hints

- The flag is hidden as ASCII text within the binary.  
- It follows this format: CCRI-AAAA-1111  
- There are five candidate flags in the file — but only ONE is correct.  
- Look for patterns carefully: some decoys are designed to mislead you.  

---

## 🛠 Tools You Might Use

- strings – Quickly extract readable text from binaries.  
- xxd – View hex and ASCII side-by-side for deeper inspection.  
- hexedit – Open the binary in an interactive hex editor for scrolling and searching.  

---

## 📝 Challenge Instructions

1. Start by running strings on hex_flag.bin to get a quick look at embedded text.  
2. Use xxd or hexedit to explore the file more carefully.  
3. Examine each candidate flag you find and determine which one matches the agency’s official format.  

Note: If you find the correct flag, save it manually:

echo "CCRI-AAAA-1111" > flag.txt

---

## 📂 Files in this folder

- hex_flag.bin – Suspicious binary to investigate.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge is about using forensics tools to pull hidden clues from binary data and separating the real target from decoys.
