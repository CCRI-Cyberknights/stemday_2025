# 📡 Challenge 13: HTTP Headers Mystery

CryptKeepers operatives have been quietly passing secret messages through internal web servers.
You have discovered **five active API endpoints** on the local network, but only **one** contains the real flag.

This challenge sharpens your ability to interact with live network services and extract intel from HTTP headers — a critical skill for penetration testers.

---

## 🧩 Your Objective

Query the active HTTP endpoints and uncover the secret hidden in the server headers.

You are looking for a custom header that looks like:

**`X-Flag: CCRI-....`**

**What to do:**
1.  Manually query each endpoint using command-line tools.
2.  Inspect the **HTTP Headers** returned by the server.
3.  Ignore the body content (HTML/JSON) and focus on the metadata.
4.  Identify the flag that matches the official format.

---

## 🌐 Target Endpoints

The intercepted services are running locally on your machine:

1.  `http://localhost:5000/mystery/endpoint_1`
2.  `http://localhost:5000/mystery/endpoint_2`
3.  `http://localhost:5000/mystery/endpoint_3`
4.  `http://localhost:5000/mystery/endpoint_4`
5.  `http://localhost:5000/mystery/endpoint_5`

---

## 🛠 Useful Tools & Techniques

Since these are live web addresses, standard file tools like `cat` or `less` won't work. You need a tool that speaks HTTP.

| Command | Description |
| :--- | :--- |
| **`curl -I <URL>`** | Fetches **Headers Only**. Perfect for this challenge. |
| `curl -v <URL>` | Verbose mode. Shows request AND response headers. |
| `curl <URL>` | Fetches the body (HTML/JSON). Useful, but the flag isn't there! |

**Example Usage:**
To inspect the headers of the first endpoint, run:

    curl -I http://localhost:5000/mystery/endpoint_1

**What to look for in the output:**

    HTTP/1.1 200 OK
    Server: CryptKeepers-Gateway/2.3.1
    Date: Mon, 25 Dec 2025 12:00:00 GMT
    Content-Type: text/html; charset=utf-8
    X-Flag: CCRI-????-????  <-- LOOK FOR THIS

---

## 🏁 Flag Format

All flags follow the official structure:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then enter the flag into the website to verify your answer.