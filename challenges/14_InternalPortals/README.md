# 🌐 Challenge 14: Internal Portals

The CryptKeeper network relies on multiple internal portals for operations.
You have identified **five internal web portals**, but only ONE of them contains the real agency flag hidden within its source code. The others are decoys.

## 🎯 Your Mission
1.  Access each internal portal via the local web server.
2.  Inspect the **HTML Source Code** of the pages.
3.  Find the hidden flag in the format:
    `CCRI-AAAA-1111`

## 🌐 Target Portals
The internal sites are mapped to these local URLs:
* `http://localhost:5000/internal/alpha`
* `http://localhost:5000/internal/beta`
* `http://localhost:5000/internal/gamma`
* `http://localhost:5000/internal/delta`
* `http://localhost:5000/internal/omega`

## 🗂️ Files in this folder
* `explore_portals.py` – A guided Python script to help you interact with the portals.
* *(Note: The pages are hosted live on the web server)*

## 💡 Hint
Developers often hide secrets in **HTML Comments** or hidden elements.
* Look for `` tags.
* The real flag starts with `CCRI-`.

## 👩‍💻 Tips & Tools
**Option 1: Use the Helper Script**
The included script allows you to open portals and scan them:

    python3 explore_portals.py

**Option 2: Browser (Manual)**
1.  Open the URL in your browser.
2.  Right-click and select **"View Page Source"** (or press `Ctrl+U`).
3.  Search (`Ctrl+F`) for "CCRI".

**Option 3: Command Line**
Use `curl` to fetch the source code and print it to the terminal:

    curl -s http://localhost:5000/internal/alpha

---
🚀 *Begin your sweep and uncover the real flag!*