# 📷 Challenge 12: QR Code Puzzle

**Mission Briefing:**
Agents intercepted a packet of digital images passed between suspected operatives.
Each file contains a QR code. While they look identical to the naked eye, they contain vastly different data.
Our intelligence suggests that four of them are decoys containing junk data or fake flags, while only one contains the valid agency flag.

## 🧠 Intelligence Report
* **The Concept:** **QR Codes** (Quick Response) are 2D barcodes that encode text, URLs, or data into a grid of black and white squares. 
* **The Strategy:** **Bulk Scanning**. You *could* scan each one with your smartphone, but that is slow and inefficient. A true analyst uses command-line tools to scan all of them instantly.
* **The Warning:** Watch out for fake flags like `QR-HINT-1234` or `SCAN-CODE-####`. The folder contains decoys.

## 📝 Investigator’s Journal
*Notes from the field:*

> "I managed to grab five images (`qr_01.png` to `qr_05.png`).
>
> Searching them one by one is tedious. I recommend using `zbarimg`. It allows you to scan image files directly from the terminal without needing a camera. If you use a wildcard (`*`), you can dump the data from all five images in a single command. The real flag will stand out immediately."

## 📂 Files in This Folder
* `qr_01.png` through `qr_05.png` – The suspicious QR code images.

---

## 🛠 Tools & Techniques

While you can use a phone, we encourage learning the terminal method.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **zbarimg** | Scans image files for barcodes/QR codes and prints the decoded text. | `zbarimg qr_01.png` |
| **Wildcard (*)** | A shell feature that lets you select multiple files at once. | `zbarimg qr_*.png` |
| **Smartphone** | The manual fallback. | *Point camera at screen* |

> 💡 **Tip:** The `zbarimg` tool outputs the type of code found (e.g., `QR-Code:`) followed by the data.
>
> Example output:
> `QR-Code:This is the hidden message`

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Scan the codes, filter the results, and identify the valid flag.