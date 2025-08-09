# 🛰️ Challenge 17: Nmap Scan Puzzle

Several suspicious services are running on the local system.  
Your job is to **scan**, **probe**, and **identify** the real agency flag hiding in plain sight.

---

## 🎯 Your Mission

1. Scan for open TCP ports on localhost in the 9000–9100 range.  
2. Investigate the responses from any open ports you find.  
3. Identify the **real** flag from among decoys and noise.  
4. Save it to a file named `flag.txt`.

---

## ⚠️ Important Clues

- Some ports respond with nonsense (junk output or developer messages).  
- Four ports will return **plausible-looking fake flags**.  
- Only **one port** contains the real flag that matches the agency's expected format.  

✅ The correct flag follows this format:  
**CCRI-AAAA-1111**

---

## 🧰 Suggested Tools & Commands

| Tool / Command                                  | Purpose                                             |
|-------------------------------------------------|-----------------------------------------------------|
| `nmap -p9000-9100 localhost`                    | Discover open ports in the specified range          |
| `nmap -sV --version-light -p9000-9100 localhost`| Identify possible service versions (optional)       |
| `curl http://localhost:PORT`                    | Retrieve response data from a specific service      |
| `nc localhost PORT`                             | Manually connect to a service for raw interaction   |
| `grep "CCRI-"` or regex                         | Help spot flag-like strings in output               |

---

## 📝 Investigation Strategy

1. Begin with an **nmap** scan to find open ports in the 8000–8100 range.
2. For each open port, use **curl** or **nc** to retrieve the service’s response.
3. Look for flag-like strings — be alert to small differences that distinguish the real one.
4. Compare responses. Not all that looks like a flag truly is one.

You may wish to jot down what each port returns in a separate file.

---

## 📂 Files in this Folder

- *(None — everything happens in the terminal)*

---

## 🏁 Flag Format

The real flag will look like:

**CCRI-AAAA-1111**

When you find it, submit it by running:

```
echo "CCRI-AAAA-1111" > flag.txt
```

(Replace `AAAA-1111` with the correct code.)

---

## 🧠 Analyst's Tip

This simulates a real-world pentest scenario:
Services often respond with unexpected data — some of it useful, some of it noise.
Train your eye to spot anomalies and patterns that reveal the truth.
