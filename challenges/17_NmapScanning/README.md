# 🛰️ Nmap Port Scanner

**Mission Briefing:**
Several simulated services are running locally on this system. Intelligence suggests they are listening on ports between **8000 and 8100**, but we do not know which ones are open or valid.

## 🧠 Intelligence Report
* **The Concept:** Before attacking a server, hackers use **Port Scanners** to knock on every "door" (port) to see which ones open.
* **The Tool:** `nmap` (Network Mapper) is the world's most famous scanner for network discovery.
* **The Warning:** Most ports in this range are closed. Some are "honeypots" returning fake data. Only one service hosts the real flag.

**Your Goal:** Scan the local network range, enumerate the open services, and identify the one carrying the flag.

## 📂 Files in this folder
*(None — all work occurs directly in the terminal via network interaction.)*

---
**🏁 Flag format:** `CCRI-AAAA-1111`