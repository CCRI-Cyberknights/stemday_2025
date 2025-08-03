# 🌐 Challenge 14: Subdomain Sweep

Liber8’s internal infrastructure spans multiple subdomains, each hosting seemingly mundane content.  
But one of them is hiding an authentic agency flag — buried somewhere in the HTML source.

---

## 🎯 Your Mission

Your task is to sweep through the HTML files from five known subdomains and identify which one conceals the real flag.

You're looking for:

**CCRI-AAAA-1111**

Only one subdomain will display a valid flag in this exact format.  
All others contain clever imitations — wrong prefixes, reversed formats, or fake agency codes.

---

## 🛠 Tools & Techniques

| Tool/Method                              | What it helps you do                                  |
|------------------------------------------|--------------------------------------------------------|
| `less *.html`                            | Scroll through raw HTML responses                      |
| `grep "CCRI-" *.html`                    | Search for possible flags by prefix                    |
| `grep -E '[A-Z]{4}-[0-9]{4}' *.html`     | Broader pattern match (might reveal fake flags)        |
| `xdg-open alpha.liber8.local.html`       | Open HTML visually in browser for formatting clues     |
| `Ctrl+U` in browser                      | View page source — some flags might not be visible     |
| `Ctrl+F` then search `CCRI`              | Find embedded data quickly in large source files       |

💡 Real security analysts know: just because you see something on the page doesn’t mean that’s how it’s structured in the source.

---

## 📝 How to Investigate

1. Inspect each `.html` file with your preferred tools.
2. Look for any text string that resembles a flag — in paragraph tags, `<pre>` blocks, or debug-style output.
3. Ignore decoys that are malformed, use other prefixes, or break the flag structure.
4. Once you confirm the correct flag, save it to a file using:

```bash
echo "CCRI-AAAA-1111" > flag.txt
````

---

## 🗂️ Files in This Folder

* alpha.liber8.local.html
* beta.liber8.local.html
* gamma.liber8.local.html
* delta.liber8.local.html
* omega.liber8.local.html

Each file represents a web page hosted on its respective internal subdomain.

---

## 🏁 Flag Format Reminder

The only valid flag will match:

**CCRI-AAAA-1111**

The rest are misleading red herrings.

---

## 🔎 Field Tip

Flags may not always be out in the open.
Scan the source code carefully — sometimes the real payload is tucked inside `<pre>` blocks or hidden behind developer comments or debug logs.

Stay sharp, agent. You're on the right track.
