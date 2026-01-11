# 🔑 Challenge 04: Vigenère Cipher

**Mission Briefing:**
You have recovered a scrambled message (`cipher.txt`) from an intercepted communication. Our analysts suspect it was encoded using the **Vigenère cipher**.

Unlike simple rotation ciphers (like ROT13), Vigenère uses a **keyword** to shift letters differently throughout the message. To break it, you need to know (or guess) that keyword.

## 🧠 Intelligence Report
* **The Cipher:** **Vigenère** is a polyalphabetic substitution cipher. 
* **The Mechanics:** It uses a keyword to shift each letter of the plaintext by a different amount. To break it, you must use the correct keyword.
* **The Clue:** The agent used a familiar word—something local. Intelligence suggests the CryptKeepers frequently use **Rhode Island city names** as encryption keywords.
* **The Warning:** The decrypted message lists **multiple flag candidates**. You must identify which one is the real flag.

## 📝 Investigator’s Journal
*Notes from the field:*

> "This isn't a simple Caesar shift. The frequency analysis is all over the place, confirming it's polyalphabetic.
>
> You need a keyword to unlock it. We know the group operates locally. I already tried 'Newport' and 'Warwick', but the output was still garbage.
>
> It must be another **major city in Rhode Island**. You might need to try a few famous ones before the text snaps into focus."

## 📂 Files in This Folder
* `cipher.txt` — The encrypted message.

---

## 🛠 Tools & Techniques

Vigenère is mathematically complex to do by hand. We recommend using a script or a robust cyber tool.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **CyberChef** | The "Swiss Army Knife" of cyber decoding. Use the "Vigenère Decode" recipe. | [GCHQ CyberChef](https://gchq.github.io/CyberChef/) |
| **Python** | You can write a script to handle the modulo math for you. | *See `vigenere_solver.py` examples online* |
| **Online Decoders** | Quickest way if you know the key. | Search "Vigenère Decoder" |

> 💡 **Tip:** In a Vigenère cipher, the letter 'A' in the plaintext might be encrypted as 'K' the first time, but as 'Z' the second time, depending on the keyword. This destroys standard letter frequency patterns.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Decrypt the message and capture the flag.