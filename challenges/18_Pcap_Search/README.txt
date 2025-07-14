# 🛰️ Challenge 18: Pcap Search

Liber8 operatives have been transmitting data across their internal network.  
You’ve intercepted a packet capture file (traffic.pcap) that may contain a hidden agency flag.

---

## 🎯 Your Mission

1. Analyze the network capture for potential flag strings.  
2. Review any candidate flags you find and determine which one is the real flag.  

---

## ⚠️ Important Notes

- Four decoy flags are embedded in the traffic to confuse investigators.  
- Only one flag matches the official CCRI format:  

✅ CCRI-AAAA-1111  

---

## 🛠 Tools You Might Use

- tshark – Command-line tool for analyzing packet captures.  
- strings – Search for readable text in the pcap file.  
- grep – Filter for flag-like patterns.  

---

## 📝 Challenge Instructions

1. Use tshark to examine the packet capture:  

   tshark -r traffic.pcap  

2. Search packet payloads for strings that resemble flags:  

   tshark -r traffic.pcap -Y "frame contains \"CCRI-\"" -T fields -e data  

3. Review any candidate flags you find. Look carefully at their format.  
4. Verify which one matches the agency’s official standard.  

Note: When you find the correct flag, save it manually:  

echo "CCRI-AAAA-1111" > flag.txt  

---

## 📂 Files in this folder

- traffic.pcap – Captured network traffic.

---

## 🏁 Flag Format

When you find the flag, it will look like this:  

CCRI-AAAA-1111  

Replace the AAAA and numbers with the real code you uncover.

---

This challenge teaches you how to inspect network traffic and extract hidden data like a packet analysis expert.
