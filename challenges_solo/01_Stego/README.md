# 🐿️ Challenge 01: Steganography Decode

Steganography is the art of hiding information inside another file — embedding messages within images, audio, or other media so that the original file appears unchanged to the average person.
Unlike encryption, which makes data unreadable, steganography aims to make data **invisible**.

---

During the Knights’ investigation into the CryptKeepers, a suspicious image was discovered.
It appears normal at first glance, but analysts believe it contains **hidden data**.

---

## 🧩 Objective

Uncover and decode `squirrel.jpg` to extract the secret message concealed inside the image.

---

## 📝 Investigator’s Journal

CryptKeepers operatives often hide things in plain sight — and they love reusing the same passwords across tools.

Not every tool will reveal something useful; some methods will lead to dead ends.
The real challenge is experimenting, correlating clues, and following the trail:

* Does the image contain suspicious metadata?
* Are there embedded files or readable strings?
* Is a password protecting the payload?
* Could the real clue be hiding in the simplest output?

Sometimes the best secrets are the ones hiding exactly where you least expect them.

---

## 🛠 Tools & Techniques

Try out the following Linux tools — each uncovers different types of hidden data:

| Tool       | Use Case                                       | Example Command                       |
| ---------- | ---------------------------------------------- | ------------------------------------- |
| `strings`  | View readable text inside binary files         | `strings squirrel.jpg \| less`        |
| `exiftool` | Inspect metadata (camera info, tags, comments) | `exiftool squirrel.jpg`               |
| `binwalk`  | Detect and extract embedded files              | `binwalk -e squirrel.jpg`             |
| `zsteg`    | Analyze LSB steganography (best for PNGs)      | `zsteg squirrel.jpg` *(may not work)* |
| `steghide` | Extract files using a passphrase               | `steghide extract -sf squirrel.jpg`   |
| `file`     | Check file type and structure                  | `file squirrel.jpg`                   |
| `xxd`      | View raw hex data                              | `xxd squirrel.jpg \| less`            |

> 💡 **Tip:** Use `man` or `--help` with any command to learn more.

---

## 📂 Files in This Folder

* `squirrel.jpg` — The suspicious image.

---

## 🏁 Flag Format

All flags follow the standard structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the code you uncover,
then submit the flag on the website to verify your answer.
