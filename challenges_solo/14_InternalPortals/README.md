# 🌐 Challenge 14: Internal Portal Audit

**Mission Briefing:**
The CryptKeepers network relies on multiple internal portals for administration. You have identified a list of **five active web pages**.
Visually, they appear to be standard maintenance pages. However, intelligence suggests that one of them contains a hidden flag hardcoded into the HTML source, invisible to the naked eye.

## 🧠 Intelligence Report
* **The Concept:** **Source Inspection**. Web browsers "render" code, turning raw HTML tags into the visual page you see. Developers often hide secrets, comments, or disabled elements (`<input type="hidden">`) in the raw code that never appear on the main screen. 
* **The Strategy:** We must bypass the visual rendering and inspect the raw code sent by the server.
* **The Tool:** `curl` is perfect for this. Unlike a browser, it prints the raw HTML directly to the terminal.
* **The Warning:** Most of the portals contain **decoy flags** hidden in the source code. You must verify which one is the real flag.

## 📝 Investigator’s Journal
*Notes from the field:*

> "I checked these pages in a browser, and they looked clean. But that's the trap—what you see isn't always what you get.
>
> Developers are lazy. They hide system IDs and debug flags in HTML comments or hidden div tags. If you just look at the screen, you'll miss it. You need to view the Page Source.
>
> Use `curl` to grab the raw code. If you see `display: none` or ``, that's where they're hiding the good stuff."

## 🌐 Target Portals
The intercepted services are running locally on your machine:
* `http://localhost:5000/internal/alpha`
* `http://localhost:5000/internal/beta`
* `http://localhost:5000/internal/gamma`
* `http://localhost:5000/internal/delta`
* `http://localhost:5000/internal/omega`

---

## 🛠 Tools & Techniques

You have two ways to inspect the source. The terminal method is faster for checking multiple pages.

| Method | Tool | Usage Example |
| :--- | :--- | :--- |
| **Command Line** | **curl** | `curl http://localhost:5000/internal/alpha` |
| **Browser** | **View Source** | Right-click the page -> **View Page Source** (or Ctrl+U). |
| **Search** | **grep** | `curl -s http://localhost:5000/internal/alpha | grep "CCRI-"` |

> 💡 **Tip:** If you are using the command line, you can check all of them quickly by using **Brace Expansion**:
> `curl http://localhost:5000/internal/{alpha,beta,gamma,delta,omega}`

---

## 🏁 Flag Format
**`CCRI-AAAA-1111`**

Retrieve the source code and find the hidden tag.