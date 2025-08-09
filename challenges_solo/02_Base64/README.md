# 📡 Intercepted Transmission: Base64 Decode Challenge

An encoded message was recovered from a compromised Liber8 field device. The file appears to contain a secure transmission — but it’s been scrambled in a way designed to pass through filters unnoticed.

Can you decode the contents and identify the real CCRI flag?

---

## 🧠 What is Base64?

Base64 is a method for encoding data into readable characters. It’s often used to send binary data (like images or documents) over text-based systems such as email or network logs.

It is **not** encryption — anyone with the right tool can decode it.

Base64-encoded content often ends in one or two `=` signs and consists of characters like `A-Z`, `a-z`, `0-9`, `+`, and `/`.

Example:  
`Q0NSSS1URVNUMC0xMjM0==` → might decode to something useful...

---

## 🛠 Tools & Techniques

Here are some tools and methods that can help decode Base64 content:

| Tool         | Use Case                          | Example Command                          |
|--------------|-----------------------------------|-------------------------------------------|
| `base64`     | Standard command-line utility     | `base64 --decode encoded.txt`            |
| `openssl`    | Cryptographic tool with Base64    | `openssl enc -d -base64 -in encoded.txt` |
| `python3`    | Script your own decoding logic    | `python3 -c "import base64; print(base64.b64decode(open('encoded.txt').read()))"` |
| `xxd`        | View file as hex dump (optional)  | `xxd encoded.txt | less`                |
| Online tools | Browser-based Base64 decoders     | *(Use with caution. Avoid uploading real flags.)* |

> Tip: If you see something readable in the decoded result — **don't overlook it**. Sometimes the message is buried in formatting or surrounded by noise.

---

## 🧩 Investigator's Journal

🗒️ *“The field agent's note was scrambled before transmission. They must have assumed the receiver knew how to reverse the signal... Lucky for us, the encoding wasn't strong — just standard issue.”*

---

## 📝 Your Objective

Inspect the contents of:

📁 **encoded.txt**

Then decode it using one of the tools above. The result may include several fake flags — only one is real. Look carefully for the **correct format**.

If your decoding tool doesn't save output to a file, you can do it manually like this:

```
echo "CCRI-AAAA-1111" > decoded_output.txt
```

---

## 📂 Files in This Folder

* `encoded.txt` — The encoded transmission.

---

## 🏁 Flag Format

The real flag follows this format:

**CCRI-AAAA-1111**

Replace `AAAA` and `1111` with the correct characters you find in the decoded message.

---

💡 Remember: Encoding is not the same as encryption. This challenge is about decoding what’s already visible — if you look at it the right way.
