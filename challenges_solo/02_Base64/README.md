# 🛰️ Challenge 02: Intercepted Transmission — Base64 Decode

Base64 is a method for encoding binary data into readable text characters.
It’s commonly used to transmit images, documents, or binary blobs across text-based channels like email or logging systems.

A recovered message from a compromised CryptKeepers field device appears to contain a secure transmission — scrambled just enough to slip past filters unnoticed.
This isn’t encryption; anyone with the right tools can decode it.

---

## 🧩 Objective

Inspect the contents of `encoded.txt`, then decode it using one of the tools listed below.

The decoded output may contain **several fake flags**. Only **one** is real.
Look closely for the flag that follows the correct agency format.

---

## 📝 Investigator’s Journal

The field agent’s message was scrambled before transmission.
They must have assumed the receiver knew how to reverse the signal…

Lucky for us, the encoding wasn’t strong — just standard issue Base64.

---

## 🛠 Tools & Techniques

Here are some useful tools for decoding Base64:

| Tool         | Use Case                               | Example Command                                                                   |
| ------------ | -------------------------------------- | --------------------------------------------------------------------------------- |
| `base64`     | Standard command-line Base64 utility   | `base64 --decode encoded.txt`                                                     |
| `openssl`    | Cryptographic tool with Base64 support | `openssl enc -d -base64 -in encoded.txt`                                          |
| `python3`    | Script your own decoding logic         | `python3 -c "import base64; print(base64.b64decode(open('encoded.txt').read()))"` |
| `xxd`        | View file as a hex dump (optional)     | `xxd encoded.txt \| less`                                                         |
| Online tools | Browser-based Base64 decoders          | *Use with caution — avoid uploading real flags.*                                  |

> 💡 **Tip:**
> If you see something readable in the decoded result, don’t overlook it.
> Sometimes the message is buried in formatting or surrounded by noise.

---

## 📂 Files in This Folder

* `encoded.txt` — The Base64-encoded transmission.

---

## 🏁 Flag Format

All flags follow this structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the code you uncover,
then input the flag into the website to verify your answer.