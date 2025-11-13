# 🔐 Challenge 03: ROT13 Decode Challenge

ROT13 is a simple substitution cipher that rotates each letter 13 positions forward in the alphabet.
After `Z`, it wraps back around to `A`.

It’s symmetrical:

* `A` → `N`
* `N` → `A`
* Apply ROT13 twice and you return to the original message.

It’s not secure — but it *is* great for confusing casual readers.

A scrambled message was intercepted from a compromised CryptKeepers communication relay.
It looks human-readable… just twisted.

---

## 🧩 Objective

Decode the message in `cipher.txt` using any of the tools below.
The decoded output may contain **multiple flag-like candidates**, but **only one** is real.

ROT13 is simple, but don’t get complacent — only one decoded flag will match the correct structure.

---

## 📝 Investigator’s Journal

They really used that childish cipher again.
At this point it’s practically a habit for them.

Run it through a rotator and see what shakes loose.

---

## 🛠 Tools & Techniques

These tools can help decode ROT13 automatically or manually:

| Tool            | Use Case                                       | Example Command                                                                         |
| --------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------- |
| `tr`            | Translate character sets using shell utilities | `tr 'A-Za-z' 'N-ZA-Mn-za-m' < cipher.txt`                                               |
| `python3`       | Use a one-liner with `codecs`                  | `python3 -c "import codecs; print(codecs.decode(open('cipher.txt').read(), 'rot_13'))"` |
| `vim` / `emacs` | ROT13 decoding built into editors              | `:%!tr A-Za-z N-ZA-Mn-za-m` *(inside Vim normal mode)*                                  |
| Online tools    | Browser-based ROT13 converters                 | *Use cautiously — avoid pasting real flags.*                                            |

> 💡 **Tip:**
> ROT13 only affects alphabetic characters (`A–Z`, `a–z`).
> Numbers, punctuation, and spacing remain unchanged.

---

## 📂 Files in This Folder

* `cipher.txt` — The scrambled transmission encoded with ROT13.

---

## 🏁 Flag Format

All flags follow the official structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the code you uncover.
Then enter the flag into the website to verify your answer.