# 🦈 PCAP Packet Analysis

You have intercepted a network file: `traffic.pcap`.
This file contains a recording of data packets transmitted across the network.

**The Concept:**
Network traffic is sent in "packets." Forensics analysts use tools like **Wireshark** or **TShark** to capture and replay these packets to find stolen credentials or secrets.

**Your Mission:** Analyze the capture.
1.  Use packet analysis tools to read the `pcap` file.
2.  Reconstruct the "TCP Streams" to read the full conversations between computers.
3.  Find the flag hidden in the transmission data.

## 📂 Files in this folder
* `traffic.pcap` – The captured network traffic file.

---
**🏁 Flag format:** `CCRI-AAAA-1111`