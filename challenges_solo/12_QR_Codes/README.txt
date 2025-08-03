# 🧠 Challenge 12: QR Code Decode

Agents intercepted a packet of digital images passed between suspected operatives.  
Each one is a QR code — a potential clue or a distraction.

Only **one** hides a valid agency flag. The rest? Misdirection.

---

## 🎯 Your Mission

Search through five suspicious QR codes and uncover which one hides a real agency flag.

✅ Real flags follow this exact format:  
**CCRI-AAAA-1111**

❌ Fake flags may look convincing but use the wrong prefix, wrong order, or incorrect structure:  
- QR-HINT-1234  
- CCRI-1111-FAKE  
- SCAN-CODE-####  
Don’t fall for imitations.

---

## 🛠 Suggested Tools

Choose your approach — command-line or visual inspection.

| Tool/Command              | Purpose                                         |
|---------------------------|--------------------------------------------------|
| `zbarimg qr_*.png`        | Scan QR images from the command line (fastest)   |
| `feh` or `eog`            | Open and visually inspect the QR code images     |
| Smartphone camera         | Scan QR codes directly off the VM screen         |
| `cat *.txt`               | If your tools save decoded text to file, view it |

> 💡 Hint: Each QR code is a PNG image. You’ll need to decode the contents to reveal any embedded text.

---

## 📝 Instructions

1. Examine all five QR codes in the folder using one of the tools above.  
2. Decode the embedded text from each image.  
3. Look carefully — some results are fake. Only one flag has the **correct format**.  
4. When you find the real flag, save it manually like this:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

---

## 📂 Files to Explore

* `qr_01.png`
* `qr_02.png`
* `qr_03.png`
* `qr_04.png`
* `qr_05.png`

Each file is a QR code image containing either a real flag or a convincing fake.

---

## 🏁 Flag Format

Real flag = `CCRI-AAAA-1111`

All other formats are designed to trick you.

---

Your forensic instincts and tool selection will determine how quickly you uncover the truth.
