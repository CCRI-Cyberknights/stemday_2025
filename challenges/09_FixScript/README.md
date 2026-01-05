# 🐛 Broken Script Challenge

**Mission Briefing:**
You have obtained a Python script (`broken_flag.py`) that is supposed to generate the secret flag.
However, the script is damaged. When run, it produces scrambled output or incorrect values.

## 🧠 Intelligence Report
* **The Problem:** The script executes, but the logic inside is flawed.
* **The Clue:** The script attempts to calculate a specific 4-digit security code using two variables (`part1` and `part2`), but the math operator seems to be wrong.
* **The Strategy:** **Debugging**.
    1.  **Read** the source code to find the math operation.
    2.  **Analyze** the variables to determine the correct operator (+, -, *, /) that produces a valid 4-digit integer.
    3.  **Edit** the script to fix the bug.

**Your Goal:** Fix the logic error in the script and run it to reveal the flag.

## 📂 Files in this folder
* `broken_flag.py` – The python script with the logic error.

---
**🏁 Flag format:** `CCRI-AAAA-1111`