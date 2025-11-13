# 📡 Challenge 18: PCAP Search

Cryptkeepers operatives have been transmitting data across their internal network.
You’ve intercepted a packet capture file: `traffic.pcap`.

Somewhere in this captured traffic lies the **real agency flag** — but several **decoys** have been planted to mislead you.

---

## 🧩 Your Objective

Inspect the packet capture and analyze its TCP traffic to uncover the real flag.

### What to Do

1. Inspect the `.pcap` file and review TCP packet flows.
2. Search for any flag-like strings inside HTTP headers, responses, or other payloads.
3. Identify all five embedded flags — **only one** follows the true agency format.
4. Validate which one is legitimate.
5. Ignore the decoys (wrong prefixes, invalid order, malformed structures).

Start simple, then go deeper:

* Run an overview scan with `tshark`.
* Use display filters to locate payloads containing text.
* Look for streams containing the substring **`CCRI-`**.
* Examine the contents of full TCP streams to reveal hidden messages.

> 🔎 **Tip:**
> Hackers often embed secret data inside otherwise normal-looking traffic.
> Your job is to sift through noise and distinguish real intel from deliberate deception.

---

## 🛠 Tools & Techniques

| Tool / Command                                          | What It Does                                       |
| ------------------------------------------------------- | -------------------------------------------------- |
| `tshark -r traffic.pcap`                                | Basic overview of packet contents                  |
| `tshark -r traffic.pcap -Y "frame contains \"CCRI-\""`  | Search for packets containing flag-like substrings |
| `tshark -r traffic.pcap -qz follow,tcp,ascii,<stream#>` | View full TCP stream contents (ASCII view)         |
| `strings traffic.pcap \| grep "CCRI-"`                  | Extract readable strings and filter for flags      |
| `grep` / `xxd`                                          | Inspect and filter raw binary data                 |
| **Wireshark** (optional)                                | GUI-based packet inspection                        |

---

## 📂 Files in This Folder

* `traffic.pcap` — Network packet capture to analyze.

---

## 🏁 Flag Format

All flags follow the official structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then input the flag into the website to verify your answer.
