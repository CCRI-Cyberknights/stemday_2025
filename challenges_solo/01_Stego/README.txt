# 🕵️ Stego Decode Challenge

Your mission: extract a secret flag hidden inside an image file.

The picture may look completely normal, but it has been altered using steganography — a technique for hiding data inside files. Cybersecurity professionals use tools to reveal these hidden secrets. Now it’s your turn.

---

## 🧠 What is Steganography?

Steganography comes from the Greek for "covered writing." It’s the practice of hiding information in plain sight, such as embedding a secret message in an image, audio file, or even text. Unlike encryption, steganography tries to avoid detection entirely.

---

## 🛠 Tools You Might Use

In Linux, there are several tools for uncovering hidden data in files. Some examples:

- steghide – extracts or embeds data in image/audio files.
- binwalk – scans files for embedded content.
- strings – searches for readable text in binary files.
- exiftool – examines metadata in media files.

This challenge assumes you’ll explore and choose the right tool for the job.

---

## 📝 Challenge Instructions

1. Start by inspecting the suspicious image:
   squirrel.jpg

2. Think about how data might be hidden:
   - Could there be hidden text?
   - A file embedded within the image?
   - Metadata carrying clues?

3. Experiment with the tools above to look deeper.

Hint: The password to unlock the secret is the most common one in the world.

---

## 📂 Files in this folder

- squirrel.jpg – The suspicious image.

Note: Some tools (like steghide) will automatically save the hidden content to a file (e.g., flag.txt). Other tools may simply print the hidden data on the screen. If you uncover the flag this way, save it yourself:

echo "CCRI-AAAA-1111" > flag.txt

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

Take your time and experiment. This challenge is about understanding the tools and thinking like a cyber detective.
