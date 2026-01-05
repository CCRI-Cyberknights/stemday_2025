# ⚙️ Binary Extraction Challenge

**Mission Briefing:**
You have recovered a compiled binary file named `hidden_flag`.

Computers read binary code easily, but humans cannot. However, developers often leave plain text strings inside compiled programs (like error messages, variable names, or secret keys).

## 🧠 Intelligence Report
* **The Lock:** The file is a binary executable, not a text file. Standard editors cannot read it.
* **The Strategy:** **Static Analysis**. We will search through the raw data bytes for readable text sequences.
* **The Tool:** The `strings` command is the industry standard for this task.

**Your Goal:** Sift through the binary noise to find the human-readable text string matching the flag format.

## 📂 Files in this folder
* `hidden_flag` – The compiled binary file containing the secret.

---
**🏁 Flag format:** `CCRI-AAAA-1111`