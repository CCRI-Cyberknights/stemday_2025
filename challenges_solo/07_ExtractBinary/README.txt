# 🔍 Extract from Binary

A suspicious binary named `hidden_flag` was found on a compromised system. Analysts believe it contains embedded clues, possibly including a real CCRI flag — but it’s hidden among decoys and junk data.

Your job is to extract all human-readable data from this binary and identify the real flag.

---

## 🧠 What’s Going On?

Compiled programs often contain strings (like messages, flags, or internal data) embedded in the binary — sometimes even if they’re never printed on screen.

These strings may be mixed with:

- Junk data
- Fake flags
- Random symbols or padding

This challenge requires a light touch of forensic analysis: pull out anything readable, sift through it, and find the one real flag.

---

## 🛠 Tools & Techniques

Here are some tools commonly used in binary string analysis:

| Tool       | Use Case                                           | Example Command                        |
|------------|----------------------------------------------------|----------------------------------------|
| `strings`  | Extract readable text from binary files            | `strings hidden_flag`                  |
| `grep`     | Filter for possible flag formats                   | `strings hidden_flag \| grep 'CCRI-'`  |
| `hexdump`  | View binary contents in hex and ASCII format       | `hexdump -C hidden_flag \| less`       |
| `xxd`      | Another hex viewer (can be reversed too)           | `xxd hidden_flag \| less`              |
| `radare2`  | Interactive disassembler for advanced exploration  | `radare2 -AA hidden_flag`              |

> Tip: Most challenges won’t require disassembly — but knowing a few patterns helps. Look for structured strings and patterns like `CCRI-XXXX-YYYY`.

---

## 🧩 Investigator’s Journal

🗒️ *“They buried the message deep in the binary. Random strings, fake markers, and padded garbage — but somewhere in there, the real one is waiting. You just have to know how to look.”*

---

## 📝 Your Objective

1. Analyze the file:
   - `hidden_flag`

2. Use string extraction tools (like `strings`, `xxd`, or `grep`) to find candidate flags.

3. There are several decoys. Only one string matches the official CCRI format.

If your tool doesn’t save output for you, you can record your finding manually:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

---

## 📂 Files in This Folder

* `hidden_flag` — The binary containing embedded flag data.

---

## 🏁 Flag Format

When you find the flag, it will follow this format:

**CCRI-AAAA-1111**

Replace `AAAA` and `1111` with the correct code.

---

💡 Use forensic reasoning and methodical exploration. The flag is there — the trick is finding it in the noise.
