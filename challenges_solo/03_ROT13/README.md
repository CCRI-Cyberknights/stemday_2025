# Challenge 3: ROT13 Decode Challenge
---

ROT13 is a basic substitution cipher that rotates each letter of the alphabet 13 positions forward. After 'Z', it wraps around back to 'A'.
It’s symmetrical:
- A becomes N  
- N becomes A  
- Apply it twice to return to the original message
This method isn't secure — but it *is* good enough to confuse casual readers.

A scrambled message was intercepted from a compromised cryptkeepers communication relay. It appears to be human-readable… but twisted.

---

## Objective: 
Use one of the tools below to decode the message and search for a string matching the flag format. The transmission may contain multiple candidates only one is real. ROT13 is one of the simplest ciphers but don't let that fool you. The message might be clear once decoded, but only one flag is authentic. 

## Investigator’s Journal:
 They used that childish cipher again. At this point, it’s just a matter of habit. Run it through the rotator and see what shakes loose. 

---

## Tools & Techniques

Here are some tools that can help you decode ROT13 manually or automatically:

| Tool         | Use Case                                 | Example Command                                      |
|--------------|------------------------------------------|------------------------------------------------------|
| `tr`         | Translate character sets in shell        | `tr 'A-Za-z' 'N-ZA-Mn-za-m' < cipher.txt`           |
| `python3`    | Use a one-liner with `codecs`            | `python3 -c "import codecs; print(codecs.decode(open('cipher.txt').read(), 'rot_13'))"` |
| `vim`/`emacs`| ROT13 decoding built into editors         | `:%!tr A-Za-z N-ZA-Mn-za-m` (inside Vim normal mode) |
| Online tools | ROT13 converters (use cautiously)         | Paste into ROT13 decoder sites (for non-sensitive data) |

> Tip: ROT13 only affects letters A–Z. Numbers, punctuation, and formatting remain unchanged.

---

## Files in This Folder

* `cipher.txt` — The scrambled transmission using ROT13.

All flags follow the same format: CCRI-AAAA-1111 Replace AAAA and the numbers with the code. Then Input the flag into the website to verify the answer.  

---
