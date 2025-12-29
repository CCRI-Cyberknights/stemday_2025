# 📡 HTTP Header Analysis

CryptKeeper operatives have been exchanging secret messages through internal HTTP servers.
You have discovered **five active API endpoints**, but only ONE contains the real agency flag.

**The Concept:**
Web servers send invisible data called **HTTP Headers** before sending the actual page content. Headers often contain technical info, cookies, or in this case, hidden secrets.

**Your Mission:** Interrogate the server.
1.  The flag is hidden in a custom header (e.g., `X-Flag`).
2.  Standard web browsers often hide these headers.
3.  Use command-line tools (like `curl -I`) or the provided scripts to inspect the headers of the endpoints below.

## 🌐 Target Endpoints
* `http://localhost:5000/mystery/endpoint_1` through `endpoint_5`

---
**🏁 Flag format:** `CCRI-AAAA-1111`