# 🧩 Vigenère Cipher Challenge

A scrambled message was extracted from a Liber8 field communication. It’s encrypted using a centuries-old cipher — one that relies on a keyword to twist each letter unpredictably.

Can you recover the original message and extract the correct CCRI flag?

---

## 🧠 What is the Vigenère Cipher?

The Vigenère cipher encrypts letters by shifting them based on a repeating keyword. Each letter of the message is moved forward in the alphabet based on the position of the corresponding letter in the keyword.

For example:  
- Plaintext: **ATTACK**  
- Keyword:   **KEYKEY**  
- Ciphertext: **KXRIGU**

The same message with a different keyword will produce a completely different result — making the key essential to successful decryption.

---

## 🛠 Tools & Techniques

Here are tools and methods that can help you decode a Vigenère cipher:

| Tool        | Use Case                               | Example Command / Link                                               |
|-------------|----------------------------------------|-----------------------------------------------------------------------|
| `python3`   | Write a simple decoder using logic     | `codecs` or manual shift logic in a Python script                    |
| Online tools| Test different keys quickly            | Search "Vigenère cipher decoder" — some support keyword input         |
| `gpg`, `cryptool`, or `cyberchef` | Advanced GUI or CLI options       | May support Vigenère (GUI required in some cases)                     |

> Tip: You’ll need the **correct keyword** to make sense of the message. The wrong key will produce garbage — but the right one reveals structure and meaning.

---

## 🧩 Investigator’s Journal

🗒️ *“The agent used a familiar word to encrypt the file — something close to home. We’ve seen them lean on regional references before. If you know where we are, you know the key.”*

---

## 📝 Your Objective

Inspect the file:

📁 **cipher.txt**

Then:
1. Try to decode the text using a keyword.
2. Look for **structured sentences** and flag-like patterns in the result.
3. One of the candidates will match the CCRI flag format — and only one will be real.

> If your decoding tool doesn’t save output to a file, you can save the correct result manually:

```
echo "CCRI-AAAA-1111" > decoded_output.txt
```

---

## 📂 Files in This Folder

* `cipher.txt` — The encrypted message using the Vigenère cipher.

---

## 🏁 Flag Format

The correct flag will appear as:

**CCRI-AAAA-1111**

Replace `AAAA` and `1111` with the flag you uncover.

---

💡 This cipher was once considered unbreakable — now it's your turn to reverse it. Think historically. Think locally.
