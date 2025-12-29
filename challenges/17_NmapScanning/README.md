# 🛰️ Nmap Port Scanner

Several simulated services are running locally on this system.
We know they are listening on ports between **8000 and 8100**, but we don't know which ones are open.

**The Concept:**
Before attacking a server, hackers use **Port Scanners** (like `nmap`) to find "open doors." Once a door is found, they interact with the service to see what it is.

**Your Mission:** Scan and Enumerate.
1.  Scan the local network range (Ports 8000–8100) to find open ports.
2.  Connect to the open ports (using `curl`) to see what they are broadcasting.
3.  Identify the one service that returns the real flag.

## ⚠️ Warning
Most ports are closed. Some return fake data. Only one is the target.

---
**🏁 Flag format:** `CCRI-AAAA-1111`