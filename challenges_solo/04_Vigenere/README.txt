# 🧩 Vigenère Cipher Challenge

You’ve recovered a scrambled message from an intercepted communication. Analysts suspect it was encoded using the Vigenère cipher — a classic encryption method that scrambles letters based on a repeating keyword.

---

## 🧠 What is the Vigenère Cipher?

The Vigenère cipher is a method of encrypting text by using a series of Caesar ciphers based on the letters of a repeating keyword. Each letter in the plaintext is shifted by an amount determined by the corresponding letter in the keyword.

For example:  
- Plaintext: ATTACK  
- Keyword:   KEYKEY  
- Ciphertext: KXRIGU  

This was considered strong in the 16th century, but modern tools can break it.

---

## 🛠 Tools You Might Use

Linux and open-source software provide ways to decode a Vigenère cipher:  

- gpg or cryptool (if available) – some cipher-breaking tools include Vigenère support.  
- python – you can write a small script to try a keyword.  
- online Vigenère decoders – useful but take care with uploading data.  

This challenge assumes you’ll explore and choose the right approach for decoding.

---

## 📝 Challenge Instructions

1. Open cipher.txt and inspect the encrypted message.  
2. Try to decode it using the suspected keyword.  

Hint: What’s the opposite of logout? That word might help unlock the message.

3. Look carefully at each decoded result. Only one will contain a flag in the correct format.

Note: Some tools might print the decoded result on screen without saving it. If you see the flag, save it yourself:  

echo "CCRI-AAAA-1111" > decoded_output.txt

---

## 📂 Files in this folder

- cipher.txt – The encrypted message.

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

Take your time and experiment. This challenge is about understanding how classical ciphers work and how they can be broken.
