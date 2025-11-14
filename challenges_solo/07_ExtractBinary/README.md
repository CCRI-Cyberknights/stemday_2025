# 🧵 Challenge 07: Extract from Binary

Compiled programs often contain embedded strings — messages, flags, or internal data — even if they’re never printed on screen.
These strings are frequently mixed with junk data, fake flags, random symbols, or padded garbage.

A suspicious binary named `hidden_flag` was recovered from a compromised system.
Analysts believe it contains embedded clues — possibly including a real flag — but it’s concealed among decoys and noise.

---

## 🧩 Objective

Extract all human-readable data from this binary and identify the **real** flag.

This challenge requires a light touch of forensic analysis:
pull out anything readable, sift through it carefully, and isolate the authentic flag.

Steps:

* Analyze the file `hidden_flag`
* Use string-extraction tools (like `strings`, `grep`, or hex viewers) to locate potential flag candidates
* Compare, validate, and eliminate decoys

---

## 📝 Investigator’s Journal

They buried the message deep inside the binary.
Random strings, fake markers, padded garbage — everything designed to distract you.

But the real one *is* in there.
You just have to know how to look.

---

## 🛠 Tools & Techniques

Tools commonly used in binary-string analysis:

| Tool      | Use Case                                      | Example Command                       |
| --------- | --------------------------------------------- | ------------------------------------- |
| `strings` | Extract human-readable text from binary files | `strings hidden_flag`                 |
| `grep`    | Filter for possible flag patterns             | `strings hidden_flag \| grep 'CCRI-'` |
| `hexdump` | View binary in hex + ASCII format             | `hexdump -C hidden_flag \| less`      |
| `xxd`     | Hex viewer (also supports reverse transforms) | `xxd hidden_flag \| less`             |
| `radare2` | Advanced disassembler for deeper exploration  | `radare2 -AA hidden_flag`             |

> 💡 **Tip:**
> Most challenges won’t require full disassembly — but knowing a few patterns helps.
> Look for structured strings resembling `CCRI-XXXX-YYYY`.

---

## 📂 Files in This Folder

* `hidden_flag` — The binary containing embedded flag data.

---

## 🏁 Flag Format

All flags follow the official structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the numbers with the correct values you uncover.
Then enter the flag into the website to verify your answer.
