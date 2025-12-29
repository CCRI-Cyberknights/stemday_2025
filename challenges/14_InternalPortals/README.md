# 🌐 Internal Portal Audit

The network relies on multiple internal portals. You have identified **five internal web pages**, but only ONE contains the flag.

**The Concept:**
What you see in a browser is just the rendered view. Developers often hide secrets, comments, or disabled elements in the **HTML Source Code**.

**Your Mission:** Inspect the Source.
1.  Access the internal portals via the local web server.
2.  Retrieve the raw HTML code (using `curl` or by viewing source).
3.  Search the code for hidden tags or comments containing the flag.

## 🌐 Target Portals
* `http://localhost:5000/internal/alpha`
* `http://localhost:5000/internal/beta`
* ...and so on (gamma, delta, omega).

---
**🏁 Flag format:** `CCRI-AAAA-1111`