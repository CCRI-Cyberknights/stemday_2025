# 🧠 Challenge 10: Metadata Mystery

You’ve recovered a suspicious image file: capybara.jpg.

It looks normal at first glance, but investigators suspect the flag is hidden in the metadata — information stored inside the file but not visible in the picture itself.

Your mission is to inspect the metadata and uncover the correct flag.

---

## 🧠 What is Metadata?

Metadata is “data about data.” In images, it often includes information like camera settings, timestamps, GPS locations, or even user comments. Attackers sometimes hide secret messages in these fields.

---

## 🛠 Tools You Might Use

- exiftool – Extracts and displays metadata from image and video files.  
- strings – Lists readable text in binary files, which sometimes includes metadata.  
- identify (from ImageMagick) – Shows basic image info.  

---

## 📝 Challenge Instructions

1. Examine capybara.jpg using exiftool or similar tools.  
2. Search through the metadata fields for any flag-like strings.  
3. Remember: the image contains 4 fake flags. Only one matches the agency’s official format and feels legitimate.  

Hint: Don’t trust the first flag you see.

Note: If your tool doesn’t save the result automatically, and you find the correct flag, save it manually:

echo "CCRI-AAAA-1111" > flag.txt

---

## 📂 Files in this folder

- capybara.jpg – Image containing hidden metadata.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge is about using forensic tools to dig beneath the surface of seemingly harmless files.
