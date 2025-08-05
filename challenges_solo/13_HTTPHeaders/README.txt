# 📡 Challenge 13: HTTP Headers Mystery

Liber8 agents have been quietly passing secret messages through web servers.  
You've intercepted five of their raw HTTP responses — but only one contains the **real** agency flag.

---

## 🎯 Your Mission

Explore the HTTP response files and uncover the secret hidden in the headers.

✅ You're looking for a header that starts with:

```

X-Flag: CCRI-....

````

Only one of the five responses has the **true** agency flag in this format:

**CCRI-AAAA-1111**

❌ Decoy flags may use similar headers, but will be disguised with:
- Invalid prefixes (e.g., `X-Code:` or `X-Flag: SCAN-1234-FAKE`)
- Incorrect formats (e.g., `CCRI-1111-AAAA`)

---

## 🛠 Useful Tools & Techniques

| Tool/Command                         | What it does                                           |
|--------------------------------------|--------------------------------------------------------|
| `less response_1.txt`                | Scroll and read a response interactively               |
| `/CCRI` inside `less`                | Search for flag-like patterns in the file              |
| `grep "X-Flag:" response_*.txt`      | Quickly scan files for any `X-Flag:` headers           |
| `grep "CCRI-" response_*.txt`        | Scan for valid flags by known prefix                   |
| `cat`, `head`, `tail`                | Peek into text files quickly                           |

> 💡 Headers are near the **top** of each HTTP response. The rest is just body content or noise.

---

## 📝 Instructions

1. Review each `response_*.txt` file using tools of your choice.  
2. Identify lines that start with `X-Flag:`.  
3. Validate whether the value follows the official flag format.  
4. When you’re sure you've found the correct flag, save it like this:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

---

## 📂 Files in This Folder

* response\_1.txt
* response\_2.txt
* response\_3.txt
* response\_4.txt
* response\_5.txt

---

## 🏁 Flag Format

The real flag matches this structure exactly:

**CCRI-AAAA-1111**

Any other variant is a deliberate fake.

---

This challenge sharpens your ability to extract intel from network traffic — a critical skill for threat analysts and penetration testers.
