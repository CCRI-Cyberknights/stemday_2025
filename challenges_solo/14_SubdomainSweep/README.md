# 🌐 Challenge 14: Subdomain Sweep

CryptKeepers' internal infrastructure spans multiple subdomains, each hosting seemingly mundane content.
But one of them is hiding an authentic agency flag — buried somewhere in the HTML source.

---

## 🧩 Your Objective

Sweep through the HTML files from **five known subdomains** and determine which one conceals the real flag.

Only **one** subdomain contains a valid flag.
All others include clever imitations using:

* Wrong prefixes
* Reversed formats
* Fake agency codes
* Incorrect or malformed structures

Inspect each `.html` file using your preferred tools. Look for any text string that resembles a flag — in `<p>` tags, `<pre>` blocks, comments, or debug-style output.

Remember:
**Flags may not be visible in the rendered page.**
Sometimes the real payload is tucked inside `<pre>` blocks, nested tags, or hidden behind developer comments.

---

## 🛠 Tools & Techniques

| Tool / Method                        | What It Helps You Do                              |
| ------------------------------------ | ------------------------------------------------- |
| `less *.html`                        | Scroll through raw HTML responses                 |
| `grep "CCRI-" *.html`                | Search for possible flags by prefix               |
| `grep -E '[A-Z]{4}-[0-9]{4}' *.html` | Broad pattern match — may reveal fakes            |
| `xdg-open alpha.cryptkeepers.local.html`   | Open an HTML file visually in a browser for clues |
| **Ctrl+U** (in browser)              | View page source — some flags may not be visible  |
| **Ctrl+F** → search `CCRI`           | Quickly locate embedded data in source code       |

> 💡 **Tip:** What you *see* in the browser isn’t always what’s actually **in the source**.
> Flags may hide inside developer comments, debug logs, deeply nested tags, or `<pre>` blocks.

---

## 📂 Files in This Folder

* `alpha.cryptkeepers.local.html`
* `beta.cryptkeepers.local.html`
* `gamma.cryptkeepers.local.html`
* `delta.cryptkeepers.local.html`
* `omega.cryptkeepers.local.html`

Each file represents a web page hosted on its respective internal subdomain.
Only one contains the genuine flag — the rest are red herrings.

---

## 🏁 Flag Format

All flags follow the official format:

**`CCRI-AAAA-1111`**

Replace `AAAA` and the digits with the correct values you uncover.
Then enter the flag into the verification website.