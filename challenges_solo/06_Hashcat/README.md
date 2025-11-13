# 🔗 Challenge 06: Hashcat ChainCrack Challenge

This challenge combines **four disciplines**:

* **Hash Cracking** — MD5 hashes are outdated and vulnerable. Tools like Hashcat can rapidly test passwords.
* **ZIP Decryption** — Each ZIP segment is locked with a password you must recover.
* **Base64 Decoding** — Every ZIP contains Base64-encoded content.
* **Flag Reassembly** — Once decoded, the fragments must be stitched back together to reveal the real flag.

CryptKeeper operatives encrypted a message and split it into three parts.
Each part is locked behind a password — and each password is hidden inside an MD5 hash.

You’ve recovered:

* `hashes.txt` — three MD5 password hashes
* `wordlist.txt` — a list of possible passwords
* `segments/` — three encrypted ZIP archives (one per password)

---

## 🧩 Objective

1. Examine the provided files.
2. Crack the MD5 hashes using a hash-cracking tool.
3. Use the recovered passwords to extract each ZIP archive.
4. Decode the extracted files from Base64.
5. Reassemble the decoded outputs to form the true flag.

---

## 📝 Investigator’s Journal

Three parts. Three locks. Three keys hidden in plain sight.
They were sloppy enough to leave the hashes — all you need to do is match them to the right passwords.

Once inside, the truth is scattered across fragments.
You’ll need to chain several techniques together: **crack → extract → decode → assemble**.

Each unlocked archive contains a scrambled segment of the final flag.
Only by piecing them together in the correct order will the true flag emerge.

---

## 🛠 Tools & Techniques

Use these tools to complete each phase of the challenge:

| Phase                | Tool                        | Example Use Case / Command                  |
| -------------------- | --------------------------- | ------------------------------------------- |
| **Crack MD5 Hashes** | `hashcat`                   | `hashcat -m 0 -a 0 hashes.txt wordlist.txt` |
|                      | `john` (`--format=raw-md5`) | Alternative cracking method                 |
| **Extract ZIPs**     | `unzip`                     | `unzip -P password segments/part1.zip`      |
| **Base64 Decode**    | `base64`                    | `base64 --decode decoded_file.txt`          |
| **Reassemble Parts** | `cat` or a Python script    | Concatenate and examine decoded segments    |

> 💡 **Tip:**
> Order matters when reassembling the final flag.
> The decoded segments represent different sections — match them carefully.

---

## 📂 Files in This Folder

* `hashes.txt` — The MD5 hashes to crack
* `wordlist.txt` — Potential password candidates
* `segments/` — Folder containing three encrypted ZIP files:

  * `part1.zip`
  * `part2.zip`
  * `part3.zip`

---

## 🏁 Flag Format

All flags follow the official structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the values you uncover.
Then enter the flag into the website to verify your answer.