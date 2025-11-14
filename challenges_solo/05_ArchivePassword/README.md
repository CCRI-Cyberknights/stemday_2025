# 🔓 Challenge 05: ZIP File Crack & Decode

Password-protected ZIP files can be brute-forced if you know — or can guess — the possible passwords.
Weak passwords, reused passwords, or predictable wordlists make cracking only a matter of time and technique.

A password-locked ZIP archive was intercepted during a CryptKeepers exfiltration attempt.
You’ve also recovered a list of likely passwords the agent tends to use.

Inside the archive is a scrambled message encoded in Base64.

---

## 🧩 Objective

Crack the ZIP, decode the message, and uncover the real flag.

### Your Tasks

1. Analyze the files:

   * `secret.zip` — the encrypted archive
   * `wordlist.txt` — the list of potential passwords

2. Brute-force the ZIP file using the provided wordlist.

3. Once the archive opens, extract `message_encoded.txt`.

4. Decode its Base64 content.

5. Inspect the decoded output and locate the **one valid flag** among possible decoys.

Unlocking the ZIP is only **phase one** — the message inside must be decoded before the flag becomes readable.

---

## 📝 Investigator’s Journal

They always use the same weak password list — lazy OPSEC at its finest.
If you’ve found the wordlist, you’re already halfway in.

This challenge is all about exploiting predictable password habits and peeling back layers of obfuscation.
Work through the outer shell before digging into the core.

---

## 🛠 Tools & Techniques

Use the following tools throughout the cracking and decoding phases:

| Phase             | Tool                   | Use Case / Command Example                              |
| ----------------- | ---------------------- | ------------------------------------------------------- |
| **ZIP Cracking**  | `fcrackzip`            | `fcrackzip -u -D -p wordlist.txt secret.zip`            |
|                   | `unzip`                | Test passwords manually: `unzip -P guess -t secret.zip` |
|                   | `python`               | Write a script to loop through password candidates      |
| **Base64 Decode** | `base64`               | `base64 --decode message_encoded.txt`                   |
|                   | `python3`              | Use `base64.b64decode()`                                |
| **Advanced**      | `zip2john` + `hashcat` | Convert ZIP to hash format, crack via GPU acceleration  |

> 💡 **Note:**
> Automated tools can sometimes corrupt a ZIP file if misused.
> Validate each attempt cleanly — especially when using scripts.

---

## 📂 Files in This Folder

* `secret.zip` — The password-protected archive
* `wordlist.txt` — The password list used for cracking

---

## 🏁 Flag Format

All flags follow the official format:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then enter the flag into the website to verify your answer.
