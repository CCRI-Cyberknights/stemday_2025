# 📡 Challenge 18: PCAP Packet Search

**Mission Briefing:**
CryptKeepers operatives have been transmitting sensitive data across their internal network.
We managed to intercept a stream of their network traffic and save it to a file (`traffic.pcap`).
Somewhere inside this recording of digital conversations lies the **real agency flag**—but they have also flooded the network with decoy packets to confuse our analysts.

## 🧠 Intelligence Report
* **The Concept:** **PCAP** (Packet Capture). When computers talk over a network, they break data into small chunks called "packets." A PCAP file is a recording of every single packet that flew across the wire. 
* **The Challenge:** The file contains thousands of packets. Most of it is technical noise.
* **The Strategy:** **Stream Reassembly**. TCP conversations happen in "streams." We need to find which stream contains the flag, and then isolate that specific conversation to read the full context.

## 📝 Investigator’s Journal
*Notes from the field:*

> "I grabbed the `traffic.pcap` file. It's full of TCP noise.
>
> My workflow for this is usually a two-step process:
> 1.  Run `strings` first to quickly see if any text stands out (like `CCRI-`). This usually gives me a hint about *what* to look for.
> 2.  Once I know what I'm looking for, I switch to `tshark`. I use it to follow the specific TCP stream where that text appeared. That way, I can see the whole conversation and verify if the flag is real or just another decoy."

## 📂 Files in This Folder
* `traffic.pcap` — The network packet capture file.

---

## 🛠 Tools & Techniques

Use `strings` for reconnaissance, and `tshark` for the deep dive.

| Step | Tool | Purpose | Usage Example |
| :--- | :--- | :--- | :--- |
| **1. Recon** | **strings** | Quickly scan the file for the flag pattern to confirm it exists and see the context. | `strings traffic.pcap \| grep "CCRI-"` |
| **2. Analysis** | **tshark** | Extract the specific packet stream. Use the `-z` flag to "follow" the conversation. | `tshark -r traffic.pcap -z follow,tcp,ascii,0` <br> *(Replace `0` with the stream number if you know it)* |
| **Alternative** | **grep** | You can also grep `tshark` output directly. | `tshark -r traffic.pcap \| grep "CCRI-"` |

> 💡 **Tip:** "Following a TCP Stream" means reconstructing the entire conversation between client and server, stripping away the network headers so you can read it like a script.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Identify the stream, follow the conversation, and capture the flag.