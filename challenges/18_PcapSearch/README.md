# 🛰️ **Challenge 18: Pcap Search**

CryptKeeper operatives have been transmitting data across their internal network. You’ve intercepted a packet capture file (`traffic.pcap`) that may contain a hidden agency flag.

🎯 **Your Mission:**
1️⃣ Run the provided helper script to analyze the network capture.
2️⃣ The script will use **tshark** to extract potential flag strings from the packet data.
3️⃣ Review the list of candidates and determine which one is the **real flag**.

⚠️ **Not every candidate is correct:**

* Four decoy flags are embedded in the traffic to confuse investigators.
* Only **one flag** matches the official CCRI format:

  ✅ **CCRI-AAAA-1111**

🛠️ **Start Here:**
Run the guided script:

./analyze_pcap.sh

The script will:

* Use **tshark** to scan packet payloads for flag-like patterns.
* Highlight each candidate found in the capture.
* Save the list of potential flags to `flag_candidates.txt` for later review.

💡 **Tip:** Look carefully at the flag format. The real flag starts with `CCRI-`. The others are clever fakes!

📂 **Files Provided:**
• `traffic.pcap` → Captured network traffic
• `analyze_pcap.sh` → Guided analysis tool

---

🚀 **Objective:** Identify the correct flag and submit it to the scoreboard.
