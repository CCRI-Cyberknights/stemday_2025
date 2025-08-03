# 🧠 Challenge 16: Hex Flag Hunter

Liber8 hackers left behind a mysterious binary: `hex_flag.bin`.

It’s too small to be a legitimate executable — which means it was likely crafted for something more… covert.

---

## 🎯 Your Mission

Use binary inspection techniques to uncover a hidden flag embedded within the file.

But beware: there are five possible candidates hidden inside.  
Only ONE of them is the true agency flag.

---

## 🧰 Recommended Tools & Commands

| Tool / Command                          | Purpose                                                |
|-----------------------------------------|--------------------------------------------------------|
| `strings hex_flag.bin`                  | Extract readable text from the binary                 |
| `grep "CCRI-"` or regex search patterns | Narrow down flag candidates                           |
| `xxd hex_flag.bin | less`               | View hex and ASCII side-by-side                       |
| `hexedit hex_flag.bin`                 | Interactively browse and search inside the file       |
| `grep -abo CCRI-` hex_flag.bin         | Show byte offsets of embedded flags (binary-aware)    |
| `dd` + `xxd`                            | Show hex context for any specific byte offset         |

💡 The correct flag will follow this format:

**CCRI-AAAA-1111**

Others may look convincing, but only one is real.

---

## 📝 Challenge Strategy

1. Start with `strings` to see what readable content is inside.
2. Search for candidate flags using `grep`, regular expressions, or visual scanning.
3. Validate which flags feel legitimate by reviewing their context (surrounding hex bytes help).
4. Consider saving promising candidates to a notes file for later review.

---

## 📂 Files in This Folder

- `hex_flag.bin` – Suspicious binary to inspect.

---

## 🏁 Flag Format

The valid flag will match this structure:

**CCRI-AAAA-1111**

Once you’ve found it, submit it by running:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

(Replace `AAAA-1111` with the real flag string.)

---

## 🧠 Final Advice

Not all flags are created equal. Some might have been inserted to throw you off.
Check the context. Think like a forensic analyst. Trust your instincts.

Your tools are sharp. Time to dissect the binary.
