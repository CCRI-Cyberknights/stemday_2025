# 🔐 Challenge 03: ROT13 Decode

**Mission Briefing:**
A scrambled message was intercepted from a compromised CryptKeepers communication relay.
It looks human-readable… just twisted. The letters seem familiar, but the words make no sense.

## 🧠 Intelligence Report
* **The Cipher:** **ROT13** (Rotate 13) is a simple substitution cipher that replaces a letter with the 13th letter after it in the alphabet. 
* **The Mechanics:** Because the alphabet has 26 letters, shifting by 13 is symmetrical. Applying the cipher twice returns the original text (`A` → `N` → `A`).
* **The Strategy:** Shift every letter back by 13 positions.
* **The Warning:** The decoded message lists **multiple flag candidates**. You must identify which one is the real flag.

## 📝 Investigator’s Journal
*Notes from the field:*

> "They really used that childish cipher again? It's not even encryption; it's just obfuscation.
>
> It looks like they tried to hide a flag in there, but ROT13 leaves numbers and symbols unchanged. If you see something like `PPEV-nnnn-1111`, that's likely the flag staring right at you, just shifted."

## 📂 Files in This Folder
* `cipher.txt` — The scrambled transmission.

---

## 🛠 Tools & Techniques

While there are many online converters, a true Linux pro uses the terminal.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **tr** | The "translate" command is perfect for swapping character sets. | `tr 'A-Za-z' 'N-ZA-Mn-za-m' < cipher.txt` |
| **Python** | Python has a built-in library for this specific cipher. | `python3 -c "import codecs; print(codecs.decode(open('cipher.txt').read(), 'rot_13'))"` |

> 💡 **Tip:** The `tr` command looks scary, but it's just a mapping:
> * `A-Za-z` = The alphabet inputs.
> * `N-ZA-Mn-za-m` = The alphabet shifted by 13.
> * It tells the computer: "Replace A with N, B with O... and N with A."

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Decode the message and find the flag in the output.