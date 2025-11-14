# 🧪 Challenge 16: Hex Flag Hunter

Cryptkeepers hackers left behind a mysterious binary: `hex_flag.bin`.
It’s far too small to be a legitimate executable — which means it was likely crafted for something more… covert.

---

## 🧩 Your Objective

Use binary inspection techniques to uncover a **hidden flag** embedded within the file.

But beware:
There are **five** possible flag candidates hidden inside.
Only **one** of them is the true Knight flag.

### How to Begin

* Start with `strings` to see any readable content inside.
* Search for candidate flags using `grep`, regex, or manual scanning.
* Validate which flags feel legitimate by reviewing their **context** — surrounding hex bytes can be very revealing.
* Save promising candidates to a notes file if needed.

Not all flags are created equal. Some are planted to mislead you.
Think like a forensic analyst. Verify before you trust.

---

## 🛠 Tools & Techniques

| Tool / Command                   | Purpose                                                   |
| -------------------------------- | --------------------------------------------------------- |
| `strings hex_flag.bin`           | Extract readable text from the binary                     |
| `grep "CCRI-"` or regex patterns | Narrow down possible flag candidates                      |
| `xxd hex_flag.bin \| less`       | View the binary’s hex and ASCII layout                    |
| `hexedit hex_flag.bin`           | Interactively browse and search inside the file           |
| `grep -abo CCRI- hex_flag.bin`   | Show byte offsets of embedded flags (binary-aware search) |
| `dd` + `xxd`                     | Display hex context around specific offsets               |

---

## 📂 Files in This Folder

* `hex_flag.bin` — Suspicious binary containing multiple embedded flags.

---

## 🏁 Flag Format

All flags follow the official structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then input the flag into the website to verify your answer.