# 🛰️ Challenge 02: Intercepted Transmission (Base64)

**Mission Briefing:**
A recovered message from a compromised CryptKeepers field device appears to contain a secure transmission. The content looks like random gibberish, but it follows a very specific pattern often used to bypass text filters.

## 🧠 Intelligence Report
* **The Concept:** **Base64** is an encoding scheme, *not* encryption. It translates binary data into a set of 64 readable characters (A-Z, a-z, 0-9, +, /). It is commonly used to send files over text channels like email. 
* **The Lock:** The text is readable but unintelligible. It usually ends with one or two equals signs (`=`) which act as padding.
* **The Strategy:** We need to reverse the encoding process to restore the original text.

## 📝 Investigator’s Journal
*Notes from the field:*

> "The field agent scrambled this message before sending it. They assumed the receiver would know how to reverse the signal.
>
> One crucial detail: The decoded output might contain **decoy flags**. I've seen them do this before—throwing in fake codes to confuse us. You need to look closely for the one that perfectly matches our agency's format (`CCRI-AAAA-1111`)."

## 📂 Files in This Folder
* `encoded.txt` — The Base64-encoded transmission.

---

## 🛠 Tools & Techniques

This is a standard encoding format, so most Linux systems have a built-in tool to handle it.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **cat** | View the file contents first to confirm it looks like Base64. | `cat encoded.txt` |
| **base64** | The standard utility for encoding/decoding. | `base64 --decode encoded.txt` |
| **Pipe (`\|`)** | Advanced technique: Send the file content directly into the decoder. | `cat encoded.txt \| base64 -d` |

> 💡 **Tip:** If the output looks like a mess of symbols *after* decoding, you might be decoding a binary file (like an image) instead of text. But in this case, we expect text. 

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Decode the file, ignore the decoys, and identify the valid flag.