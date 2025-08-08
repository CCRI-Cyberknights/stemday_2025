# 🛰️ Challenge 18: Pcap Search

Liber8 operatives have been transmitting data across their internal network.  
You’ve intercepted a packet capture file: `traffic.pcap`.

Somewhere in this captured traffic lies the real agency flag. But beware — decoys are in place.

---

## 🎯 Your Mission

1. Inspect the `.pcap` file and analyze its TCP traffic.
2. Search for any flag-like strings in HTTP headers or responses.
3. Identify the **real** flag from among decoys.

---

## ⚠️ What You Should Know

- There are **five flags** embedded in the network traffic.  
- **Four are decoys** — inserted to mislead you.  
- Only **one** is valid: it follows the official flag format.  

✅ The correct flag will look like this:  
**CCRI-AAAA-1111**

---

## 🛠 Tools You Might Use

| Tool / Command | What it Does |
|----------------|--------------|
| `tshark -r traffic.pcap` | Basic overview of packet contents |
| `tshark -r traffic.pcap -Y "frame contains \"CCRI-\""` | Search for flag strings |
| `tshark -r traffic.pcap -qz follow,tcp,ascii,<stream#>` | View contents of TCP stream |
| `strings traffic.pcap | grep "CCRI-"` | Look for embedded flags as ASCII |
| `grep` / `xxd` | Inspect and filter binary content |
| `wireshark traffic.pcap` (optional) | GUI inspection of all packets |

---

## 📝 Challenge Instructions

1. Start by running a simple `tshark` scan to view packets.
2. Use filters to narrow down TCP payloads that might contain text data.
3. Look specifically for streams containing strings like `CCRI-`.
4. Validate which flag is real — be cautious, the fake ones are intentionally misleading.

Once you've found the real flag, save it like this:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

(Replace `AAAA-1111` with your discovered flag.)

---

## 📂 Files in this folder

* `traffic.pcap` — Network packet capture to analyze

---

## 🏁 Flag Format

The real flag will match this pattern:

**CCRI-AAAA-1111**

(4 capital letters, then 4 digits — separated by hyphens)

---

## 🧠 Forensic Tip

Hackers often try to mask their data inside common traffic patterns.
Your job is to sift through the noise and recognize real flags from clever decoys.
Think like an analyst. Search, filter, and verify.
