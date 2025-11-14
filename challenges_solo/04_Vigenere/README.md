# 🔑 Challenge 04: Vigenère Cipher Challenge

The Vigenère cipher encrypts text by shifting each letter according to a repeating keyword.
Every letter in the plaintext is moved forward in the alphabet based on the corresponding letter of the keyword.

For example:

```
Plaintext: ATTACK
Keyword:   KEYKEY
Ciphertext: KXRIGU
```

Using a different keyword produces a completely different ciphertext — making the **key** essential to successful decryption.

---

## 🧩 Objective

Recover the original message and extract the correct flag.

1. Inspect `cipher.txt`.
2. Decode the text using an appropriate keyword.
3. Look for readable sentences and flag-like patterns in the decrypted result.

This cipher once earned the nickname “the unbreakable cipher.”
Now it’s your turn to reverse it.

---

## 📝 Investigator’s Journal

The agent used a familiar word — something close to home.
We’ve seen the CryptKeepers lean on **regional references** before.

If you know where we are… you know the key.

---

## 🛠 Tools & Techniques

Here are tools that can help decode a Vigenère cipher:

| Tool                           | Use Case                                 | Example / Description                                            |
| ------------------------------ | ---------------------------------------- | ---------------------------------------------------------------- |
| `python3`                      | Write your own decoder using shift logic | Use `codecs`, string arithmetic, or a custom Python script       |
| Online tools                   | Quickly test different keywords          | Search “Vigenère Cipher Decoder”                                 |
| `gpg`, `cryptool`, `CyberChef` | Advanced GUI/CLI options                 | Some tools offer built-in Vigenère decoding (GUI often required) |

> 💡 **Tip:**
> The **correct keyword** makes the message snap into clarity.
> The wrong one produces only noise.

---

## 📂 Files in This Folder

* `cipher.txt` — The message encrypted using the Vigenère cipher.

---

## 🏁 Flag Format

All flags follow the official structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the code you uncover.
Then enter the flag into the website to verify your answer.