# 🌐 Challenge 14: Internal Portals

CryptKeepers' internal infrastructure spans multiple virtual portals, each hosting seemingly mundane content. But one of them is hiding an authentic agency flag — buried deep within the document structure.

---

## 🧩 Your Objective

Access the internal sites and determine which one conceals the real flag.

Only **one** portal contains a valid flag. All others include decoy flags or no flags at all.

You must inspect the **DOM (Document Object Model)** or **Page Source** for each site. Look for hidden elements or debug-style data that doesn't appear on the rendered page.

Remember:
**The real flag is hidden from plain sight.**
It may be tucked inside hidden tags, metadata blocks, or developer-only spans that are not visible during normal browsing.

---

## 🛠 Tools & Techniques

| Tool / Method                        | What It Helps You Do                              |
| ------------------------------------ | ------------------------------------------------- |
| **Ctrl+U** (in browser)              | View Page Source — reveals hidden tags            |
| **F12** or **Inspect Element** | Open DevTools to explore the DOM tree             |
| `curl <URL> | grep "CCRI-"`         | Search the source code via command line           |
| **Ctrl+F** → search `CCRI`           | Quickly locate embedded data in the source        |

> 💡 **Tip:** Just because the page looks empty doesn't mean it is. 
> Developers often hide "debug info" or "system IDs" in tags with `display: none` or hidden attributes.

---

## 📂 Portals to Inspect

When the local web server is running, you can access the portals at these local URLs:

* **Alpha Portal**: `http://localhost:5000/internal/alpha`
* **Beta Portal**: `http://localhost:5000/internal/beta`
* **Gamma Portal**: `http://localhost:5000/internal/gamma`
* **Delta Portal**: `http://localhost:5000/internal/delta`
* **Omega Portal**: `http://localhost:5000/internal/omega`

Only one contains the genuine flag. The rest are red herrings designed to waste your time.

---

## 🏁 Flag Format

All flags follow the official format:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then enter the flag into the verification website.