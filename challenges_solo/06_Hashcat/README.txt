# 🔓 Hashcat ChainCrack Challenge

Liber8 operatives encrypted a message and split it into parts. Each part is locked behind a password, and each password is hidden inside an MD5 hash. You've recovered:

- 🔐 `hashes.txt`: 3 password hashes  
- 🗒️ `wordlist.txt`: Possible passwords  
- 📦 `segments/`: Three ZIP archives (one per password)

Each archive, once unlocked, contains a scrambled part of a flag. Your job: crack the hashes, extract and decode the segments, and reassemble the true CCRI flag.

---

## 🧠 What’s Going On?

This challenge combines multiple skills:

1. **Hash Cracking** — MD5 hashes are outdated and vulnerable. Tools like Hashcat can rapidly test passwords against them.
2. **ZIP Decryption** — The password-protected ZIP segments must be unlocked using the cracked passwords.
3. **Base64 Decoding** — Each ZIP contains Base64-encoded content.
4. **Flag Reassembly** — After decoding, you'll need to piece the segments back together and identify the real flag.

---

## 🛠 Tools & Techniques

Here’s a selection of tools that may help you complete each phase:

| Phase               | Tool         | Example Use Case / Command                                          |
|--------------------|--------------|---------------------------------------------------------------------|
| Crack MD5 Hashes    | `hashcat`    | `hashcat -m 0 -a 0 hashes.txt wordlist.txt`                         |
|                    | `john` + `--format=raw-md5` | Alternative cracking approach                                 |
| Extract ZIPs       | `unzip`      | `unzip -P password segments/part1.zip`                              |
| Base64 Decoding    | `base64`     | `base64 --decode decoded_file.txt`                                  |
| Reassemble Segments| `cat` or script | Concatenate decoded parts and review them                           |

> Tip: Order matters when reassembling the flag. The decoded parts likely correspond to different sections of the flag.

---

## 🧩 Investigator’s Journal

🗒️ *“Three parts. Three locks. Three keys hidden in plain sight. They were sloppy enough to leave the hashes — all you need to do is match them to the right keys. Once inside, the truth is scattered across the fragments.”*

---

## 📝 Your Objective

1. Examine the following files:
   - `hashes.txt` — contains the 3 MD5 hashes.
   - `wordlist.txt` — contains the potential passwords.
   - `segments/` — contains the encrypted ZIPs.

2. Crack the hashes using a hash cracking tool.

3. Use the recovered passwords to extract each ZIP archive.

4. Decode each extracted file using Base64.

5. Reassemble the decoded outputs to form possible flags.

6. Only one flag will follow the official CCRI format.

> If your tools print the final flag on screen, don’t forget to save it:

```bash
echo "CCRI-AAAA-1111" > final_flag.txt
````

---

## 📂 Files in This Folder

* `hashes.txt` — List of MD5 hashes to crack
* `wordlist.txt` — Potential password candidates
* `segments/` — Folder containing 3 encrypted ZIP files (part1.zip, part2.zip, part3.zip)

---

## 🏁 Flag Format

The correct flag will look like this:

**CCRI-AAAA-1111**

Replace `AAAA` and `1111` with the values you uncover.

---

💡 This challenge rewards persistence and precision. You’ll need to chain together several techniques — crack, extract, decode, and reconstruct — to reveal the hidden message.
