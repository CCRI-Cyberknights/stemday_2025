# 🐿️ Challenge 01: Steganography Decode

**Mission Briefing:**
During the Knights’ investigation into the CryptKeepers, a suspicious image (`squirrel.jpg`) was recovered from a public server.
Visually, it appears to be a standard photograph of a rodent. However, our analysts have flagged it for containing **hidden data**.

## 🧠 Intelligence Report
* **The Concept:** **Steganography** is the art of hiding information inside another file (like an image or audio track) so that the original appears unchanged to the naked eye. Unlike encryption, which makes data unreadable, steganography makes data **invisible**. 
* **The Lock:** The secret message is likely embedded within the pixel data itself, protected by a passphrase.
* **The Strategy:** We need a tool capable of parsing the image structure to extract the payload.

## 📝 Investigator’s Journal
*Notes from the field:*

> "CryptKeepers operatives hide things in plain sight. I've noticed they get lazy with their security—they often reuse simple passwords or leave the password blank entirely.
>
> I tried running `strings` on it first, but I just got binary garbage. I have a hunch they used a tool like `steghide` to embed the message. The real challenge isn't just running the tool; it's guessing the password. If it asks for one, try the obvious stuff first."

## 📂 Files in This Folder
* `squirrel.jpg` — The suspicious image file.

---

## 🛠 Tools & Techniques

To solve this manually, you will need to use Linux terminal tools. Here are the standard methods for analyzing suspicious images:

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **steghide** | The industry standard for JPG steganography. It requires a password to extract data. | `steghide extract -sf squirrel.jpg` |
| **strings** | Scans the file for readable text. Useful if the flag is not encrypted, just embedded. | `strings squirrel.jpg` |
| **exiftool** | Views metadata (Camera model, timestamps, comments). | `exiftool squirrel.jpg` |
| **binwalk** | Checks if other files (like a ZIP) are glued to the end of the image. | `binwalk -e squirrel.jpg` |

> 💡 **Tip:** When `steghide` asks for a passphrase, if you don't know it, try pressing **ENTER** (empty password) or guessing simple words related to the image content. 

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Once you extract the hidden text file, read its contents to find the flag.