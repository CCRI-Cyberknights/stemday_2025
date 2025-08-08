# 🕵️ Stego Decode Challenge

A suspicious image has surfaced during a Liber8 investigation. Intelligence analysts believe it contains hidden data that may expose an insider’s identity.

Your job: extract the secret message embedded within this image.

---

## 🧠 What is Steganography?

Steganography is the art of hiding messages in plain sight — like embedding a text file inside an image or song. Unlike encryption, its goal is to be invisible rather than unreadable.

---

## 🛠 Tools & Techniques

Try out some of these Linux tools — each reveals different kinds of secrets:

| Tool      | Use Case                                              | Example Command                      |
|-----------|--------------------------------------------------------|--------------------------------------|
| `strings` | View readable text inside binary files                | `strings squirrel.jpg | less`       |
| `exiftool`| Inspect metadata (camera info, author, hidden tags)   | `exiftool squirrel.jpg`              |
| `binwalk` | Detect and extract embedded files                     | `binwalk -e squirrel.jpg`            |
| `zsteg`   | Analyze LSB steganography in PNGs (JPG support limited)| `zsteg squirrel.jpg *(may not work here)*` |
| `steghide`| Embed/extract files using a passphrase                | `steghide extract -sf squirrel.jpg`  |
| `file`    | Check file type and structure                         | `file squirrel.jpg`                  |
| `xxd`     | View raw hex data                                     | `xxd squirrel.jpg | less`           |

> Tip: Use `man` or `--help` with any command to learn more.

Not all of these tools will reveal useful information — some may lead to dead ends. The challenge lies in experimenting and connecting the dots.

---

## 🧩 Investigator's Journal

🗒️ *“Liber8 operatives often hide things in plain sight... and they tend to reuse the same password across tools. Predictable, rebellious, and catchy — that’s their style.”*

---

## 📝 Your Objective

Analyze the image:

📁 **squirrel.jpg**

Ask yourself:
- Does the image contain metadata or embedded content?
- Are there readable strings or hidden files inside?
- Might a password be needed to reveal the payload?

If you discover the flag in output or extract a file, be sure to save it manually:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

---

## 📂 Files in This Folder

* `squirrel.jpg` — The image to investigate.

---

## 🏁 Flag Format

All flags follow the same format:

**CCRI-AAAA-1111**

Replace `AAAA` and the numbers with the code you uncover.

---

💡 This challenge rewards persistence and creative use of tools. Think like a cyber detective — sometimes the best secrets are the ones hiding in plain sight.