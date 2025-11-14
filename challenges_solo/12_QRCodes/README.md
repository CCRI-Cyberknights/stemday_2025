# 📷 Challenge 12: QR Code Decode

Agents intercepted a packet of digital images passed between suspected operatives.
Each one is a QR code — a potential clue… or a distraction.

Only **one** hides a valid knight’s flag.
The rest? Pure misdirection.

---

## 🧩 Your Objective

Search through **five suspicious QR codes** and uncover which one contains the real flag.

Fake flags may look convincing but will use the wrong prefix, wrong order, or an invalid structure such as:

* `QR-HINT-1234`
* `CCRI-1111-FAKE`
* `SCAN-CODE-####`

Don’t fall for imitations.

### What to Do

1. Examine all five QR codes using the tools of your choice.
2. Decode the embedded text from each image.
3. Compare the outputs — some will be fake.
4. Only one decoded result follows the correct flag format.

---

## 🛠 Suggested Tools

Choose whichever approach fits your investigative style:

| Tool / Command     | Purpose                                                   |
| ------------------ | --------------------------------------------------------- |
| `zbarimg qr_*.png` | Scan and decode QR images from the command line (fastest) |
| `feh` or `eog`     | Visually inspect the QR codes                             |
| Smartphone camera  | Scan QR codes directly from the VM screen                 |
| `cat *.txt`        | View decoded text if your tools write output to files     |

> 💡 **Hint:** Each QR code is a PNG image. You’ll need to decode the contents to reveal any embedded text.

---

## 📂 Files in This Folder

* `qr_01.png`
* `qr_02.png`
* `qr_03.png`
* `qr_04.png`
* `qr_05.png`

---

## 🏁 Flag Format

All flags follow the official format:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the numbers with the correct values you uncover.
Then enter the flag into the website to verify your answer.
