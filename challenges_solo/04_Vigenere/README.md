# Challenge 4: Vigenère Cipher Challenge
---

Vigenère cipher encrypts letters by shifting them based on a repeating keyword. Each letter of the message is moved forward in the alphabet based on the position of the corresponding letter in the keyword. 

For example: 

    Plaintext: ATTACK 

    Keyword: KEYKEY 

    Ciphertext: KXRIGU 

The same message with a different keyword will produce a completely different result making the key essential to successful decryption.

## Objective:
 recover the original message and extract the correct flag. This type of cipher was once considered unbreakable now it's your turn to reverse it. 
-  Inspect the file cipher.txt 
- Try to decode the text using a keyword. 
- Look for structured sentences and flag-like patterns in the result. 

## Investigator’s Journal: 
The agent used a familiar word to encrypt the file something close to home. We’ve seen them lean on regional references before. If you know where we are, you know the key. 
 
---

## Tools & Techniques

Here are tools and methods that can help you decode a Vigenère cipher:

| Tool        | Use Case                               | Example Command / Link                                               |
|-------------|----------------------------------------|-----------------------------------------------------------------------|
| `python3`   | Write a simple decoder using logic     | `codecs` or manual shift logic in a Python script                    |
| Online tools| Test different keys quickly            | Search "Vigenère cipher decoder" — some support keyword input         |
| `gpg`, `cryptool`, or `cyberchef` | Advanced GUI or CLI options       | May support Vigenère (GUI required in some cases)                     |

> Tip: You’ll need the **correct keyword** to make sense of the message. The wrong key will produce garbage but the right one reveals structure and meaning.

---

##  Files in This Folder

* `cipher.txt` — The encrypted message using the Vigenère cipher.
 
All flags follow the same format: CCRI-AAAA-1111 Replace AAAA and the numbers with the code you uncover Input the flag into the website to verify the answer.

---


