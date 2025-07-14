# 🛰️ Challenge 17: Nmap Scan Puzzle

Several simulated services are running locally on this system.  
Your mission is to uncover the real flag hidden among them.

---

## 🎯 Your Mission

1. Scan for open ports in the range 8000–8100.  
2. Explore the discovered services and inspect their responses.  
3. Identify the one true flag and save it.

---

## ⚠️ Important Notes

- Not every open port contains a flag:  
  • Some return random junk text (e.g., error pages, developer APIs).  
  • Four ports return decoy flags with slightly wrong formats.  
  • Only **one port** contains the real flag.  

✅ The correct flag follows this format: CCRI-AAAA-1111

---

## 🛠 Tools You Might Use

- nmap – Scan the system for open ports in a specified range.  
- curl – Connect to services and retrieve their responses.  
- netcat (nc) – Manually interact with services on specific ports.  

---

## 📝 Challenge Instructions

1. Use nmap to scan the local system for open ports:  

   nmap -p8000-8100 127.0.0.1  

2. Review the list of open ports and explore each one with curl or netcat.  
3. Look for flag-like strings in the responses.  
4. Verify the format carefully — only one flag matches the agency’s standard.  

Note: When you find the correct flag, save it manually:  

echo "CCRI-AAAA-1111" > flag.txt

---

## 📂 Files in this folder

- No scripts provided — explore manually using the tools above.

---

## 🏁 Flag Format

When you find the flag, it will look like this:  

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge teaches you how to discover and probe network services like a penetration tester.
