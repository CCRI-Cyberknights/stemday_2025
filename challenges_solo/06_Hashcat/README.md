# 🔓 Challenge 06: Hashcat ChainCrack

**Mission Briefing:**
You have intercepted **3 encrypted archive segments** from a data exfiltration attempt. Each segment (`part1.zip`, `part2.zip`, `part3.zip`) is locked with a different password.
However, we also found a file (`hashes.txt`) containing the **MD5 hashes** of those passwords.

## 🧠 Intelligence Report
* **The Lock:** Three separate ZIP files, each requiring a unique password.
* **The Keys:** The passwords are hidden behind MD5 hashes. You cannot use the hash directly; you must "crack" it to reveal the plaintext password. 
* **The Strategy:** **Chain Reaction**. You must link multiple forensic techniques together:
    1.  **Crack:** Reverse the hashes to find the passwords.
    2.  **Unlock:** Use the passwords to extract the archives.
    3.  **Assemble:** The extracted files are fragments. Combine them to reveal the flag.
* **The Warning:** Once reassembled, the data will yield **multiple potential flags**. Only one is valid.

## 📝 Investigator’s Journal
*Notes from the field:*

> "Three parts. Three locks. Three keys hidden in plain sight.
>
> They were sloppy enough to leave the hashes, but they didn't leave the passwords. You'll need to run a dictionary attack against those MD5s.
>
> Once you're inside, don't expect the flag to just be sitting there. It looks like they split the file into pieces. You'll have to stitch the decoded fragments back together to make sense of it. Order matters."

## 📂 Files in This Folder
* `hashes.txt` — The list of target MD5 hashes.
* `wordlist.txt` — A list of candidate passwords.
* `segments/` — A folder containing the three encrypted ZIP files.

---

## 🛠 Tools & Techniques

This challenge requires a pipeline of tools.

| Phase | Tool | Usage Example |
| :--- | :--- | :--- |
| **1. Crack** | **hashcat** | `hashcat -m 0 -a 0 hashes.txt wordlist.txt` <br> *(`-m 0` = MD5 mode, `-a 0` = Wordlist mode)* |
| **2. Unlock** | **unzip** | `unzip -P [password] segments/part1.zip` |
| **3. Decode** | **base64** | `base64 -d extracted_file.txt` |
| **4. Assemble** | **cat** | Combine the text outputs manually or use a script. |

> 💡 **Tip:** Hashcat requires a GPU to run fast, but for this small wordlist, it will run instantly on any CPU. If `hashcat` fails to run, you can also use `john --format=raw-md5 hashes.txt`.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Crack the hashes, unlock the zips, decode the fragments, and assemble the flag.