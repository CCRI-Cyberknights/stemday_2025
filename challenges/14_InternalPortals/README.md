# 🌐 Internal Portal Audit

**Mission Briefing:**
The network relies on multiple internal portals for administration. You have identified a list of **five active web pages**, but only ONE contains the hidden flag.

## 🧠 Intelligence Report
* **The Concept:** What you see in a web browser is the "rendered" view. Developers often hide secrets, comments, or disabled elements in the raw **HTML Source Code** which are invisible on the main screen.
* **The Strategy:** **Source Inspection**. You must bypass the visual rendering and inspect the raw code sent by the server.
* **The Tool:** `curl` is perfect for this. Unlike a browser, it prints the raw HTML directly to the terminal.
* **The Warning:** Beware of **fake flags** hidden in the source code of the decoy portals.

**Your Goal:** Retrieve the raw HTML from the portals and search the code for hidden tags or comments containing the real flag.

## 🌐 Target Portals
The intercepted services are running locally on your machine:
* `http://localhost:5000/internal/alpha`
* `http://localhost:5000/internal/beta`
* `http://localhost:5000/internal/gamma`
* `http://localhost:5000/internal/delta`
* `http://localhost:5000/internal/omega`

---
**🏁 Flag format:** `CCRI-AAAA-1111`