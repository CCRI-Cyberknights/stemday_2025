# 📡 HTTP Header Analysis

**Mission Briefing:**
CryptKeeper operatives have been exchanging secret messages through internal HTTP servers.
You have discovered **five active API endpoints** on the local network, but only ONE contains the real agency flag.

## 🧠 Intelligence Report
* **The Concept:** Web servers send invisible data called **HTTP Headers** before sending the actual page content.
* **The Lock:** The flag is hidden in a custom header (e.g., `X-Flag` or `Secret-Key`). Standard browsers often hide these.
* **The Tool:** `curl` (Client URL) is the standard tool for interacting with web servers. Using the `-I` flag fetches *only* the headers.
* **The Warning:** Most of the endpoints are decoys returning **fake flags**.

**Your Goal:** Interrogate the endpoints to find the hidden header with the real flag.

## 🌐 Target Endpoints
The intercepted services are running locally on your machine:
1.  `http://localhost:5000/mystery/endpoint_1`
2.  `http://localhost:5000/mystery/endpoint_2`
3.  `http://localhost:5000/mystery/endpoint_3`
4.  `http://localhost:5000/mystery/endpoint_4`
5.  `http://localhost:5000/mystery/endpoint_5`

---
**🏁 Flag format:** `CCRI-AAAA-1111`