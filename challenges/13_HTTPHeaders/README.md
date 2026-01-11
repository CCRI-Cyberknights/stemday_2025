# 📡 HTTP Header Analysis

**Mission Briefing:**
CryptKeeper operatives have been exchanging secret messages through internal HTTP servers.
You have discovered a server log file identifying **five active API endpoints**, but only ONE contains the real agency flag.

## 🧠 Intelligence Report
* **The Concept:** Web servers send invisible data called **HTTP Headers** before sending the actual page content.
* **The Lock:** The flag is hidden in a custom header (e.g., `X-Flag` or `Secret-Key`). Standard browsers often hide these.
* **The Tool:** `curl` (Client URL) is the standard tool for interacting with web servers. Using the `-I` flag fetches *only* the headers.
* **The Warning:** Most of the endpoints are decoys returning **fake flags**.

**Your Goal:** Interrogate the endpoints found in the logs to find the hidden header with the real flag.

## 📂 Files in this folder
* `server_logs.txt` – Intercepted logs listing the active endpoints.

---
**🏁 Flag format:** `CCRI-AAAA-1111`