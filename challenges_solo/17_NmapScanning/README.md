# 📡 Challenge 17: Nmap Scan Puzzle

**Mission Briefing:**
CryptKeepers operatives are hosting several rogue services on this system to communicate with their botnet.
We know these services are listening on local TCP ports in the **9000–9100** range.
Your mission is to scan the network, identify the active "doors" (ports), and interrogate each service to find the one carrying the valid agency flag.

## 🧠 Intelligence Report
* **The Concept:** **Port Scanning**. Computers use "ports" (numbered 1–65535) to manage network connections. Think of an IP address as a building and ports as the apartment numbers.
* **The Tool:** **Nmap** (Network Mapper). It knocks on every door in a specified range to see which ones are open. 
* **The Strategy:**
    1.  **Scan:** Find the open ports between 9000 and 9100.
    2.  **Connect:** Use `curl` or `nc` (Netcat) to talk to the services running on those ports.
    3.  **Filter:** Distinguish the real flag from the decoys.

## 📝 Investigator’s Journal
*Notes from the field:*

> "I know they are hiding in the 9000s. If you scan the whole machine, it'll take too long. Focus your Nmap scan on `9000-9100`.
>
> Once you see the open ports, you have to manually check them. Some might just send garbage data. Others might send fake flags like `CCRI-FAKE-...`. You need to grab the output from the right one and save it to a file named `flag.txt`."

## 📂 Files in This Folder
*(None — all work occurs directly in the terminal via network interaction.)*

---

## 🛠 Tools & Techniques

You are mapping the digital terrain.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **nmap** | The industry standard scanner. `-p` specifies the range. | `nmap -p 9000-9100 localhost` |
| **curl** | Connects to web-based ports (HTTP). | `curl http://localhost:9001` |
| **nc** | "Netcat". Connects to raw TCP ports. Use this if `curl` fails. | `nc localhost 9001` |
| **Output Redirection** | Save your findings to the required file. | `echo "CCRI-AAAA-1111" > flag.txt` |

> 💡 **Tip:** Nmap output looks like this:
> ```text
> PORT     STATE SERVICE
> 9001/tcp open  tor-orport
> 9050/tcp open  tor-socks
> ```
> Each "open" line is a target you need to investigate.

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Scan the range, interrogate the ports, and identify the true flag.