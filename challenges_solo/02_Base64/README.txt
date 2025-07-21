# 🧩 Base64 Decode Challenge

You’ve intercepted a suspicious message from a compromised system.

The file encoded.txt contains a block of strange-looking text. The pattern suggests Base64, a common encoding scheme that turns binary data into readable characters.

---

## 🧠 What is Base64?

Base64 is not encryption. It’s just a way to encode binary data into a set of readable characters so it can be safely sent over text-based systems. Anyone with the right tool can decode it.

Base64-encoded text often looks like random letters, numbers, and symbols ending in one or two equal signs (e.g., `Q0NSSS1URVNUMC0xMjM0==`).

---

## 🛠 Tools You Might Use

Linux provides several ways to decode Base64 data. Some examples:

- base64 – the standard utility for encoding and decoding Base64 data.
- python – using `base64.b64decode()` in a quick script.
- openssl – can also perform Base64 decoding.
- online tools – can decode Base64 in a browser (but be careful what you upload).

---

## 📝 Challenge Instructions

1. Open encoded.txt and inspect the contents.
2. Use one of the tools above to decode the message.
3. Look carefully at the result for the flag.

Note: Some tools can write the decoded content directly to a file. If yours doesn’t, and you see the flag printed on screen, save it manually:

echo "CCRI-AAAA-1111" > decoded_output.txt

---

## 📂 Files in this folder

- encoded.txt – The encoded message.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

Take your time and experiment. This challenge is about understanding encoding and learning how to reverse it.
