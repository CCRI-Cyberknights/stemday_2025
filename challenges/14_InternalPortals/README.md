# 🌐 Challenge 14: Internal Portals

The CryptKeeper network relies on multiple internal portals for operations. You have identified **five internal web portals**, but only ONE of them contains the real agency flag hidden within its source code. The others are decoys.

## 🎯 Your Mission
1.  Access each internal portal via the local web server.
2.  Inspect the **HTML Source Code** or **DOM structure** of the pages.
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
* *(Note: The pages are hosted live on the web server)*

## 💡 Hint
Developers often hide secrets in **hidden elements** or internal system tags.
* Look for elements that aren't visible on the main screen (like tags with `display: none`).
* The real flag starts with `CCRI-`.


🚀 *Investigate the portals and uncover the authentic flag!*