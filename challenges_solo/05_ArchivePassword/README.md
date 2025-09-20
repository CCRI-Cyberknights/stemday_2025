# Challenge 5: ZIP File Crack & Decode
---

Password-protected ZIP files can be brute-forced if you know (or guess) the possible passwords. If weak passwords are used or if you have a list of likely candidates cracking is just a matter of time and technique. 

An encrypted ZIP archive was intercepted during a Cryptkeepers exfiltration attempt. It’s locked with a password, but you’ve also recovered a list of possible passwords most likely used by the same agent. Inside the archive is a scrambled message, encoded in Base64.

## Objective: 
Crack the ZIP, decode the message, and uncover the real flag. 

   - Analyze the following files: 
secret.zip: the encrypted archive 
wordlist.txt: the list of possible passwords 

   - Brute-force the ZIP file with the wordlist until it opens. 

   -  Once extracted, decode the contents of message_encoded.txt (Base64). 

   -  From the decoded message, locate the one valid flag.
 
unlocking the archive is only part one. The extracted file contains Base64-encoded content you'll need to decode it before the flag becomes readable.

## Investigator’s Journal:
They always used the same weak password list lazy opsec. If you find that list, you’ve already got the key. Just try them until something opens. This challenge is about exploiting weak password practices and layered obfuscation. Think like an analyst work the outer shell before you reach the core. 

---

## Tools & Techniques

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


---

##  Files in This Folder

* `secret.zip` — The password-protected archive
* `wordlist.txt` — The password list for cracking

All flags follow the same format: CCRI-AAAA-1111 Replace AAAA and the numbers with the code you uncover Input the flag into the website to verify the answer. 

---

