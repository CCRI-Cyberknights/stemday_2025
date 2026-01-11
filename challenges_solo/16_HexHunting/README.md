# 🧪 Challenge 16: Hex Flag Hunter

**Mission Briefing:**
CryptKeepers hackers left behind a mysterious binary file (`hex_flag.bin`).
It is far too small to be a functional program. Our analysts believe it was crafted specifically to smuggle data past our filters.

## 🧠 Intelligence Report
* **The Concept:** **Hexadecimal Dumps**. Computer files are just sequences of numbers (bytes). A "Hex Dump" allows a human to view the raw data.
* **The View:** Tools like `xxd` divide the screen into three columns:
    1.  **Offset:** Where you are in the file (like line numbers).
    2.  **Hex:** The raw data (e.g., `41 42 43`).
    3.  **ASCII:** The text translation (e.g., `A B C`). 
* **The Strategy:** You need to look at the ASCII column to find the flag, but also check the Hex column for context.
* **The Warning:** Buried inside the raw bytes are **five possible flags**. Only **one** is real; the others are traps.

## 📝 Investigator’s Journal
*Notes from the field:*

> "Strings alone might not cut it here. I ran `strings` and saw five different flags.
>
> You need to look closer. Open the file in a Hex Viewer. Sometimes the 'real' flag is surrounded by a specific pattern of bytes, or located at a specific offset, while the fakes are just random junk.
>
> Don't trust the first thing you see. Verify the pattern."

## 📂 Files in This Folder
* `hex_flag.bin` — The suspicious binary file.

---

## 🛠 Tools & Techniques

To see the matrix, you need a hex viewer.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **xxd** | The standard command-line hex viewer. | `xxd hex_flag.bin | less` |
| **hexdump** | Canonical hex dump tool. The `-C` flag makes it readable. | `hexdump -C hex_flag.bin | less` |
| **grep** | You can still search for text inside the binary. | `grep -a "CCRI-" hex_flag.bin` |
| **hexedit** | (Optional) Allows you to scroll and edit the hex in real-time. | `hexedit hex_flag.bin` |

> 💡 **Tip:** In `xxd` output:
> ```text
> 00000000: 4343 5249 2d54 4553 5431 2d31 3233 34  CCRI-TEST1-1234
> ```
> The right side is readable text. The middle is the code.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Analyze the hex dump, compare the candidates, and identify the true flag.