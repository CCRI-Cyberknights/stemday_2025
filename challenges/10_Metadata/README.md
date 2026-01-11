# 📷 Metadata Explorer

**Mission Briefing:**
You have intercepted an image: `capybara.jpg`.
Visually, it is just a picture of a cute animal. However, digital files contain "data about data," known as **Metadata**.

Metadata often includes the camera model, GPS coordinates, timestamps, or hidden comments added by the creator.

## 🧠 Intelligence Report
* **The Lock:** The information is hidden in the file header (EXIF tags), not visible in the image itself.
* **The Strategy:** **Metadata Extraction**. We need to read the headers to see what's hidden behind the pixels.
* **The Tool:** `exiftool` is the industry standard for reading and writing file metadata.
* **The Warning:** This file contains **decoy flags**. Verify that the flag you find matches the standard format.

**Your Goal:** Extract the metadata, filter through the noise to ignore decoys, and find the real flag.

## 📂 Files in this folder
* `capybara.jpg` – The image file containing hidden metadata.

---
**🏁 Flag format:** `CCRI-AAAA-1111`