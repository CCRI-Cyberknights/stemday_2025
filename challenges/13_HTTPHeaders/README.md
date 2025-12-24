# 📡 Challenge 13: HTTP Headers Mystery

CryptKeeper operatives have been exchanging secret messages through internal HTTP servers.
You’ve discovered **five active API endpoints** on the local network, but only ONE contains the real agency flag. The others are decoys designed to mislead intruders.

## 🎯 Your Mission
1.  Interrogate each HTTP endpoint running on your local server.
2.  Look for a hidden `X-Flag:` header in the response.
3.  Identify the correct flag in this format:
    `CCRI-AAAA-1111`

## 🌐 Target Endpoints
The intercepted services are accessible at:
* `http://localhost:5000/mystery/endpoint_1`
* `http://localhost:5000/mystery/endpoint_2`
* `http://localhost:5000/mystery/endpoint_3`
* `http://localhost:5000/mystery/endpoint_4`
* `http://localhost:5000/mystery/endpoint_5`

## 🗂️ Files in this folder
* `investigate_headers.py` – A guided Python script to help you interact with the endpoints.
* *(Note: The endpoints are hosted live on the web server, they are not text files)*

## 💡 Hint
Only one flag starts with `CCRI-`. All others use fake prefixes.

## 👩‍💻 Tips & Tools
Since these are live network services, you cannot use file tools like `cat` or `less`.

**Option 1: Use the Helper Script**
The included script provides a menu to scan the endpoints:

    python3 investigate_headers.py

**Option 2: Use `curl` (Manual Mode)**
Use the `-I` flag to fetch **headers only** (without downloading the body):

    curl -I http://localhost:5000/mystery/endpoint_1

---
🚀 *Ready to uncover the hidden flag?*