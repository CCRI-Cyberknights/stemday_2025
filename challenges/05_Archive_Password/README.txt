# 🔐 ZIP File Crack & Decode

You’ve recovered a mysterious ZIP archive: secret.zip.

It’s password-protected — and the password isn’t obvious. Luckily, a wordlist of possible passwords (wordlist.txt) was also found. Only one of them works.

Inside the archive lies a Base64-encoded message. It contains several flag-like strings, but only one matches the official agency format.

---

## 🧠 What’s Going On?

Password-protected ZIP archives are a common way to secure files. However, if the password is weak or if you have a list of potential passwords, it’s possible to “brute-force” your way in.

After cracking the archive, you’ll also need to decode the extracted Base64 message to uncover the flag.

---

## 🛠 Tools You Might Use

To attempt cracking the ZIP file:  

- fcrackzip – a tool to brute-force ZIP passwords using a wordlist.  
- unzip – if you already know the password.  
- python – you can write a script to try each word in the list.  

To decode Base64 content:  

- base64 – standard Linux utility.  
- python – `base64.b64decode()`  

---

## 📝 Challenge Instructions

1. Start by examining secret.zip and wordlist.txt.  
2. Use one of the tools above to try each password in the wordlist.  
3. Once you unlock the archive, extract its contents.  
4. Decode the extracted message and carefully review for the correct flag.

Note: Some tools will print the decoded result on screen instead of saving it. If you see the flag, save it yourself:  

echo "CCRI-AAAA-1111" > decoded_output.txt

---

## 📂 Files in this folder

- secret.zip – The password-protected archive.  
- wordlist.txt – Potential passwords.  

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge is about learning how weak passwords can be exploited and how data can be hidden inside archives.
