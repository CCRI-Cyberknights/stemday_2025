# 🧩 Base64 Decode Challenge

**📡 Intercepted Transmission**
An encoded message has been intercepted from a compromised system. The file `encoded.txt` contains data obfuscated using **Base64**.

## 🧠 Mission Briefing
**Base64 is NOT encryption.** It is a common encoding scheme used to represent binary data as text.
* **The Signature:** Base64 strings consist of random alphanumeric characters and almost always end with one or two equals signs (`=` or `==`) as padding.
* **The Tools:** Linux has a built-in tool called `base64` specifically for reversing this.

**Your Goal:** Confirm the file matches the signature, then decode it to retrieve the flag.

## 📂 Files in this folder
* `encoded.txt` – The intercepted Base64-encoded transmission.

---
**🏁 Flag format:** `CCRI-AAAA-1111`