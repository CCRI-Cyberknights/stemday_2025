# 📱 QR Code Puzzle

**Mission Briefing:**
You have recovered a set of QR (Quick Response) codes.
QR codes are just a visual way of encoding text data. One of these images contains the agency flag; the others are decoys or broken links.

## 🧠 Intelligence Report
* **The Lock:** The data is encoded visually in 2D barcodes.
* **The Strategy:** **Bulk Scanning**. You have multiple images, and checking them one by one on a phone is inefficient.
* **The Tool:** Command-line tools like `zbarimg` allow you to scan image files directly in the terminal without a camera.

**Your Goal:** Scan the images, filter the output, and find the one that decodes to a valid flag.

## 📂 Files in this folder
* `qr_01.png` to `qr_05.png` – Image files containing QR codes.

---
**🏁 Flag format:** `CCRI-AAAA-1111`