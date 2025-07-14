# 🔐 ROT13 Decode Challenge

An intercepted note was found in the logs of a compromised account. It’s readable… sort of. But every letter seems slightly off — like the alphabet has been twisted.

This challenge introduces ROT13, a simple substitution cipher that shifts each letter 13 places through the alphabet.

- It’s symmetrical: applying ROT13 twice restores the original message.  
- While not secure by today’s standards, it’s still used to obscure text from casual readers.

---

## 🧠 What is ROT13?

ROT13 (“rotate by 13 places”) is a classic Caesar cipher where each letter is replaced with the letter 13 positions later in the alphabet. For example:  

A → N  
N → A  
HELLO → URYYB  

Apply ROT13 twice and you’ll get back the original message.

---

## 🛠 Tools You Might Use

Linux provides multiple ways to decode ROT13 text:  

- tr – translate characters in the terminal (e.g., `tr 'A-Za-z' 'N-ZA-Mn-za-m'`)  
- python – using `codecs.decode(message, 'rot_13')`.  
- online ROT13 decoders – easy but requires caution with sensitive data.  

---

## 📝 Challenge Instructions

1. Open cipher.txt and inspect the scrambled message.  
2. Use one of the tools above to decode it back into readable text.  
3. Search the decoded text for the hidden flag.

Note: Some tools will print the decoded message on screen without saving it. If you spot the flag, save it manually:

echo "CCRI-AAAA-1111" > decoded_output.txt

---

## 📂 Files in this folder

- cipher.txt – The scrambled message.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

Take your time and experiment. This challenge is about learning how to reverse basic ciphers.
