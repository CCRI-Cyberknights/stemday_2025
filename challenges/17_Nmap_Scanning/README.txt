🛰️ Challenge #17 – Nmap Scan Puzzle
--------------------------------------

Several mysterious services are running on this system.

Your mission is to:

1️⃣ Scan localhost (**127.0.0.1**) for open ports in the range **8000–8100**.  
2️⃣ Connect to each discovered service and inspect the responses.  
3️⃣ Identify the **REAL flag** and submit it to the scoreboard.

⚠️ Not every open port contains a flag:
- Some ports return random junk text (e.g., error pages, dev APIs).
- Four ports return **decoy flags** with slightly wrong formats.
- Only **one port** contains the **REAL flag** in this format:

🎯 Flag Format:

CCRI-AAAA-1111

🔧 **Tools Available:**
- Nmap
- curl
- A web browser

💡 **Hints:**
- Limit your scan to **ports 8000–8100** for faster results.
- You can check a port using `curl`, for example:

curl http://localhost:<port>


