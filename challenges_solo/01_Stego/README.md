# 🐿️ Challenge 01: Steganography Decode

**Mission Briefing:**
During the Knights’ investigation into the CryptKeepers, a suspicious image (`squirrel.jpg`) was recovered from a public server.
Visually, it appears to be a standard photograph of a rodent. However, our analysts have flagged it for containing **hidden data**.

## 🧠 Intelligence Report
* **The Concept:** **Steganography** is the art of hiding information inside another file (like an image or audio track) so that the original appears unchanged to the naked eye. Unlike encryption, which makes data unreadable, steganography makes data **invisible**. 
* **The Lock:** The secret message is likely embedded within the pixel data itself, protected by a passphrase.
* **The Strategy:** We need a tool capable of parsing the image structure to extract the payload.
* **The Warning:** The hidden file inside the image contains **multiple flag candidates**. Verify which one is the real flag.

## 📝 Investigator’s Journal
*Notes from the field:*

> "CryptKeepers operatives are sloppy with their passwords. They often leave hints inside the file's **metadata** (comments, authors, etc.) because they can't remember them.
>
> I tried running `strings` on it first, but I just got binary garbage. I have a hunch they used `steghide` to embed the message. The extraction will fail without the exact passphrase, so check the file headers before you start guessing blindly."

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

> 💡 **Tip:** If you don't know the passphrase, do not guess randomly. Use `exiftool` to inspect the image's tags for a clue.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Once you extract the hidden text file, read its contents to find the flag.