# 📡 Challenge 17: Nmap Scan Puzzle

Several suspicious services are running on the local system.
Your mission: **scan, probe, and identify the real agency flag hiding in plain sight.**

---

## 🧩 Your Objective

1. Scan for open **TCP ports on localhost** in the **9000–9100** range.
2. Investigate the responses from any open ports.
3. Identify the *real* flag among decoys and noise.
4. Save the correct flag into a file named `flag.txt`.

---

## 🛠 Investigation Steps

* Begin with an **Nmap scan** of the port range.
* For each open port, use `curl` or `nc` to retrieve the service’s response.
* Look carefully for flag-like strings — even minor differences matter.
* Compare responses across ports.
* Four ports will return **plausible fake flags**.
* Other ports may return nonsense or developer notes.
* Only **one** port contains a flag matching the agency’s official format.

You may find it helpful to record each port’s response in a separate notes file.

> 🔎 **Tip:**
> This simulates a real-world pentest scenario — services often return unexpected data.
> Train your eye to spot anomalies and subtle clues.

---

## 🛠 Tools & Techniques

| Tool / Command                                   | Purpose                                         |
| ------------------------------------------------ | ----------------------------------------------- |
| `nmap -p9000-9100 localhost`                     | Discover open ports in the specified range      |
| `nmap -sV --version-light -p9000-9100 localhost` | Optionally identify service versions            |
| `curl http://localhost:PORT`                     | Retrieve response data from a specific port     |
| `nc localhost PORT`                              | Manually interact with a service for raw output |
| `grep "CCRI-"` or regex filters                  | Spot flag-like strings in output                |

---

## 📂 Files in This Folder

*(None — all work occurs directly in the terminal.)*

---

## 🏁 Flag Format

All flags follow the official format:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Enter the flag into the website to verify your answer.