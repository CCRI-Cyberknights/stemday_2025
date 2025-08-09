# 🔐 ZIP File Crack & Decode

An encrypted ZIP archive was intercepted during a Liber8 exfiltration attempt. It’s locked with a password, but you’ve also recovered a list of possible passwords nearby — probably used by the same operative.

Inside the archive? A scrambled message, encoded in Base64. Your mission is to crack the ZIP, decode the message, and uncover the real flag.

---

## 🧠 What’s Going On?

Password-protected ZIP files can be brute-forced if you know (or guess) the possible passwords. If weak passwords are used — or if you have a list of likely candidates — cracking is just a matter of time and technique.

But unlocking the archive is only part one. The extracted file contains Base64-encoded content — you'll need to decode it before the flag becomes readable.

---

## 🛠 Tools & Techniques

Try using a combination of these tools for different phases of this challenge:

| Phase           | Tool         | Use Case / Command Example                                   |
|------------------|--------------|---------------------------------------------------------------|
| ZIP Cracking     | `fcrackzip`  | `fcrackzip -u -D -p wordlist.txt secret.zip`                 |
|                  | `unzip`      | Test passwords one by one: `unzip -P guess -t secret.zip`    |
|                  | `python`     | Write a script to loop through wordlist                      |
| Base64 Decoding  | `base64`     | `base64 --decode message_encoded.txt`                        |
|                  | `python3`    | `base64.b64decode()`                                         |
| Optional Tools   | `zip2john` + `hashcat` | For hash-based cracking (advanced)              |

> Note: Be cautious with automation. Rate limits or malformed attempts might corrupt the ZIP file during testing. Validate each attempt cleanly.

---

## 🧩 Investigator’s Journal

🗒️ *“They always used the same weak password list — lazy opsec. If you find that list, you’ve already got the key. Just try them until something opens.”*

---

## 📝 Your Objective

1. Analyze the following files:
   - `secret.zip`: the encrypted archive
   - `wordlist.txt`: the list of possible passwords

2. Brute-force the ZIP file with the wordlist until it opens.

3. Once extracted, decode the contents of `message_encoded.txt` (Base64).

4. From the decoded message, locate the **one valid CCRI flag**.

> If your decoder prints the flag on screen, you can save it like this:

```
echo "CCRI-AAAA-1111" > decoded_output.txt
```

---

## 📂 Files in This Folder

* `secret.zip` — The password-protected archive
* `wordlist.txt` — The password list for cracking

---

## 🏁 Flag Format

When you find the flag, it will follow this format:

**CCRI-AAAA-1111**

Replace `AAAA` and `1111` with the real code you uncover in the decoded message.

---

💡 This challenge is about exploiting weak password practices and layered obfuscation. Think like an analyst — work the outer shell before you reach the core.
