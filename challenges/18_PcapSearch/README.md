# 🦈 PCAP Packet Analysis

**Mission Briefing:**
You have intercepted a network file: `traffic.pcap`.
This file contains a recording of data packets transmitted across the network during a suspicious event.

## 🧠 Intelligence Report
* **The Concept:** Network traffic is broken into small chunks called "packets." Forensics analysts capture these to replay conversations later.
* **The Strategy:** **Stream Reconstruction**. Instead of looking at individual packets, we want to reassemble the "TCP Stream" to read the full conversation as if we were there.
* **The Tool:** `tshark` (Terminal Wireshark) is the command-line version of the world's most popular packet analyzer.
* **The Warning:** The capture file contains **decoy traffic** and fake flags. You must distinguish the real flag from the noise.

**Your Goal:** Read the capture file, identify the stream containing the real flag, and reconstruct the conversation.

## 📂 Files in this folder
* `traffic.pcap` – The captured network traffic file.

---
**🏁 Flag format:** `CCRI-AAAA-1111`