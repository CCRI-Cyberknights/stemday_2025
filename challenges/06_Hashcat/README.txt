# 🔓 Hashcat ChainCrack

You’ve intercepted 3 encrypted archive segments — each one locked behind a password. Alongside them, you found:

- hashes.txt – A list of MD5 hashes hiding the passwords.  
- wordlist.txt – Likely password candidates.  

Your task is to crack the hashes, extract the segments, decode them, and assemble the final flag.

---

## 🧠 What’s Going On?

This challenge combines multiple cybersecurity skills:  

1. **Hash cracking:** MD5 is a hashing algorithm often used to store passwords. It’s not secure, and tools like Hashcat can attempt millions of guesses quickly.  
2. **Archive extraction:** Each segment is a password-protected ZIP file.  
3. **Base64 decoding:** The extracted files are encoded and need decoding.  
4. **Flag assembly:** After decoding, you’ll find several possible flags. Only one fits the correct format.

---

## 🛠 Tools You Might Use

- hashcat – powerful GPU-accelerated hash cracking tool.  
- fcrackzip – to brute-force ZIP passwords (if needed).  
- base64 – standard Linux utility for decoding Base64 data.  
- cat – to concatenate multiple decoded parts into a single flag.  

---

## 📝 Challenge Instructions

1. Start by examining hashes.txt and wordlist.txt.  
2. Use Hashcat (or another cracking tool) to recover the 3 passwords from their MD5 hashes.  
3. Unlock each encrypted ZIP segment using the cracked passwords.  
4. Decode the Base64 data in each segment.  
5. Assemble the decoded parts into possible flags and determine which one matches the correct format.

Note: If a tool doesn’t save the result for you, and you see the correct flag, save it yourself:

echo "CCRI-AAAA-1111" > final_flag.txt

---

## 📂 Files in this folder

- hashes.txt – 3 MD5 hashes to crack.  
- wordlist.txt – Possible passwords.  
- segments/ – Folder with 3 encrypted ZIP files.  

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge will test your ability to chain together multiple steps to uncover the truth.
