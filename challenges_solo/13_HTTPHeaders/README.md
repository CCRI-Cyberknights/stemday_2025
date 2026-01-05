# 📡 Challenge 13: HTTP Header Analysis

**Mission Briefing:**
CryptKeepers operatives have been exchanging secret messages through internal HTTP servers.
You have discovered **five active API endpoints** on the local network. While they all serve generic web pages, our intelligence suggests that ONE of them is transmitting the agency flag in a covert channel.

## 🧠 Intelligence Report
* **The Concept:** **HTTP Headers**. When you visit a website, the server sends a block of invisible metadata *before* it sends the actual page content (HTML). This includes data like `Server Type`, `Date`, and `Cookies`. 
* **The Lock:** The flag is hidden in a **Custom Header** (e.g., `X-Flag` or `Secret-Key`). Standard web browsers often hide these headers from the user.
* **The Strategy:** **Headless Interaction**. We will use a command-line tool to talk to the server directly and request *only* the headers.

## 📝 Investigator’s Journal
*Notes from the field:*

> "I found five active endpoints running on `localhost:5000`.
>
> If you just open them in a browser, you won't see anything. The secret isn't on the page; it's in the handshake. You need to inspect the HTTP response headers. Look for anything suspicious starting with `X-`.
>
> Use `curl` with the `-I` flag. It tells the server 'I only want the headers, keep the body'."

## 🌐 Target Endpoints
The intercepted services are running locally on your machine:
1.  `http://localhost:5000/mystery/endpoint_1`
2.  `http://localhost:5000/mystery/endpoint_2`
3.  `http://localhost:5000/mystery/endpoint_3`
4.  `http://localhost:5000/mystery/endpoint_4`
5.  `http://localhost:5000/mystery/endpoint_5`

---

## 🛠 Tools & Techniques

Since these are live web addresses, standard file tools like `cat` won't work.

| Tool | Purpose | Usage Example |
| :--- | :--- | :--- |
| **curl -I** | **Fetch Headers Only**. This is the key command. | `curl -I http://localhost:5000/mystery/endpoint_1` |
| **curl -v** | **Verbose Mode**. Shows the entire request/response conversation. | `curl -v http://localhost:5000/mystery/endpoint_1` |
| **Browser DevTools** | You can also press F12 in a browser and check the "Network" tab, but the terminal is faster. | *N/A* |

> 💡 **Tip:** Example output of `curl -I`:
> ```text
> HTTP/1.0 200 OK
> Server: Werkzeug/2.0.3 Python/3.10
> Content-Type: text/html; charset=utf-8
> X-Flag: CCRI-????-????   <-- TARGET ACQUIRED
> ```

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Interrogate the endpoints and capture the header.