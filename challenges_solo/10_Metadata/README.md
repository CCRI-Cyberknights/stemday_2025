# 🖼️ Challenge 10: Metadata Mystery

**Mission Briefing:**
You have recovered a suspicious image file (`capybara.jpg`) from a server used by the **CryptKeepers**.
At first glance, it seems harmless—just a goofy animal photo.
However, investigators believe a CryptKeeper operative embedded a flag inside the image’s **metadata** to pass it to a handler without raising suspicion.

## 🧠 Intelligence Report
* **The Concept:** **Metadata** is "data about data." For images, this includes camera settings, GPS coordinates, authors, and comments. 
* **The Lock:** The information isn't in the pixels; it's in the file header. Opening the image in a viewer won't reveal it.
* **The Warning:** This file contains **four fake flags** and only **one real flag**. The enemy knows we are watching and planted decoys.

## 📝 Investigator’s Journal
*Notes from the field:*

> "These guys love hiding stuff in the `Comment` or `Author` tags. I've seen them use `exiftool` to inject fake flags into standard fields like 'Camera Model' just to waste our time.
>
> You need to dump *all* the metadata and sift through it. The real flag will follow the strict agency format (`CCRI-AAAA-1111`). If a flag looks weird or has the wrong format, it's bait."

## 📂 Files in This Folder
* `capybara.jpg` — The image hiding the data.

---

## 🛠 Tools & Techniques

We need a tool that looks *at* the file properties, not *inside* the image.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **exiftool** | The industry standard for reading/writing metadata. | `exiftool capybara.jpg` |
| **identify** | Part of ImageMagick; shows basic details. | `identify -verbose capybara.jpg` |
| **grep** | Use this to filter the output for the flag format. | `exiftool capybara.jpg \| grep "CCRI"` |

> 💡 **Tip:** Some metadata fields are obscure. Don't just look at the top few lines; scroll through the entire output.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Extract the metadata, ignore the decoys, and find the true flag.