# 🌐 Challenge 13: HTTP Headers Mystery

Cryptkeepers agents have been quietly passing secret messages through web servers.
You’ve intercepted **five raw HTTP responses**, but only **one** contains the real flag.

This challenge sharpens your ability to extract intel from network traffic — a critical skill for both threat analysts and penetration testers.

---

## 🧩 Your Objective

Explore the HTTP response files and uncover the secret hidden in the headers.

You are looking for a header that starts with:

**`X-Flag: CCRI-....`**

What to do:

1. Review each `response_*.txt` file using your preferred tools.
2. Identify any lines beginning with `X-Flag:`.
3. Validate whether the value follows the official flag structure.
4. Ignore decoys that mimic the pattern but use the wrong format.

Decoy flags may attempt to mislead using:

* **Invalid prefixes**

  * `X-Code:`
  * `X-Flag: SCAN-1234-FAKE`
* **Incorrect flag formats**

  * `CCRI-1111-AAAA`
  * non-matching patterns

---

## 🛠 Useful Tools & Techniques

| Tool / Command                  | What It Does                                |
| ------------------------------- | ------------------------------------------- |
| `less response_1.txt`           | Scroll and read a response interactively    |
| `/CCRI` *(inside `less`)*       | Search for flag-like patterns               |
| `grep "X-Flag:" response_*.txt` | Quickly scan for any `X-Flag:` headers      |
| `grep "CCRI-" response_*.txt`   | Scan for values using the known flag prefix |
| `cat`, `head`, `tail`           | Quickly peek into text files                |

> 💡 **Tip:** HTTP headers appear near the *top* of each response.
> The rest is just page content or noise.

---

## 📂 Files in This Folder

* `response_1.txt`
* `response_2.txt`
* `response_3.txt`
* `response_4.txt`
* `response_5.txt`

---

## 🏁 Flag Format

All flags follow the official structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then enter the flag into the website to verify your answer.
