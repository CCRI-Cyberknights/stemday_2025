# 🔓 Challenge 05: ZIP File Crack

**Mission Briefing:**
You have recovered a mysterious ZIP archive (`secret.zip`) from a CryptKeepers exfiltration attempt. It is locked with a password.
However, during the data recovery, we also found a text file (`wordlist.txt`) containing thousands of potential passwords used by the agent.

## 🧠 Intelligence Report
* **The Lock:** Standard ZIP encryption.
* **The Strategy:** **Dictionary Attack**. Instead of guessing random characters, we will automate the process of trying every single word in the provided list until one works. 
* **The Twist:** Unlocking the ZIP is only Phase 1. Inside, you will find a scrambled text file that requires further decoding (Base64).

## 📝 Investigator’s Journal
*Notes from the field:*

> "Lazy OPSEC at its finest. They always reuse the same weak passwords from this specific list.
>
> You don't need to be a genius to break this; you just need to be persistent. If you have `wordlist.txt`, you already have the key—you just need a tool to find which specific line opens the lock. Once you're inside, don't celebrate yet. The payload is likely encoded again."

## 📂 Files in This Folder
* `secret.zip` — The password-protected archive.
* `wordlist.txt` — A list of common passwords to attempt.

---

## 🛠 Tools & Techniques

While you *could* try passwords manually, automation is the key here.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **fcrackzip** | A fast ZIP password cracker. The `-D` flag tells it to use a dictionary (wordlist). | `fcrackzip -u -D -p wordlist.txt secret.zip` |
| **John the Ripper** | Advanced cracking tool. Requires converting the zip to a hash first. | `zip2john secret.zip > hash.txt` then `john hash.txt` |
| **Bash / Python** | You can script a loop to try passwords using the standard `unzip` command. | *Scripting required (for loops)* |
| **Base64** | Once the zip is open, use this to decode the inner message. | `base64 -d message.txt` |

> 💡 **Tip:** If you are using `fcrackzip`, the `-u` flag is important—it verifies the password actually works by trying to unzip the file. Without it, the tool might give false positives.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Crack the zip, extract the file, decode the message, and find the flag.