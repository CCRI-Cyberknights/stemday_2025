# Challenge 2: Intercepted Transmission Base64 Decode  
---
Base64 is a method for encoding data into readable characters. It’s often used to send binary data (like images or documents) over text-based systems such as email or network logs. 

An encoded message was recovered from a compromised cryptkeepeers field device. The file appears to contain a secure transmission, but it’s been scrambled in a way designed to pass through filters unnoticed. It is not encryption; anyone with the right tool can decode it. 

## Objective: 
Inspect the contents of encoded.txt then decode it using one of the tools below. The result may include several fake flags; only one is real. Look carefully for the correct format. 

## Investigator's Journal: 
The field agent's note was scrambled before transmission. They must have assumed the receiver knew how to reverse the signal... Lucky for us, the encoding wasn't strong, just standard issue.

---

## Tools & Techniques

Here are some tools and methods that can help decode Base64 content:

| Tool         | Use Case                          | Example Command                          |
|--------------|-----------------------------------|-------------------------------------------|
| `base64`     | Standard command-line utility     | `base64 --decode encoded.txt`            |
| `openssl`    | Cryptographic tool with Base64    | `openssl enc -d -base64 -in encoded.txt` |
| `python3`    | Script your own decoding logic    | `python3 -c "import base64; print(base64.b64decode(open('encoded.txt').read()))"` |
| `xxd`        | View file as hex dump (optional)  | `xxd encoded.txt | less`                |
| Online tools | Browser-based Base64 decoders     | *(Use with caution. Avoid uploading real flags.)* |

> Tip: If you see something readable in the decoded result **don't overlook it**. Sometimes the message is buried in formatting or surrounded by noise.

---

## Files in This Folder

* `encoded.txt` — The  base64 encoded transmission.

All flags follow the same format: CCRI-AAAA-1111 Replace AAAA and the numbers with the code. Then Input the flag into the website to verify the answer.  

---

