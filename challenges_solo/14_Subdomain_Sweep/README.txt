# 🌐 Challenge 14: Subdomain Sweep

The Liber8 network relies on multiple subdomains for internal operations.  
You’ve intercepted DNS data revealing five subdomains, each hosting a web page that displays a “flag.” But only ONE of these flags is authentic — the others are clever decoys.

---

## 🎯 Your Mission

1. Investigate each subdomain’s page.  
2. Examine the flag text displayed on the page.  
3. Identify which flag is real using the agency’s format.

---

## 🛠 Tools You Might Use

- less – View the raw HTML content of each page.  
- grep – Search for flag-like patterns in multiple files (e.g., `grep "CCRI-" *.html`).  
- a web browser – Open each page visually to inspect how the flag is displayed.  

---

## 📝 Challenge Instructions

1. Open and review each subdomain HTML file one by one.  
2. Look for text strings that resemble a flag.  
3. Remember: only one flag follows the official agency format. Fake flags will use the wrong prefixes or structures.  

Note: If you find the correct flag, save it manually:

echo "CCRI-AAAA-1111" > flag.txt

---

## 🗂️ Files in this folder

- alpha.liber8.local.html – Subdomain page #1  
- beta.liber8.local.html – Subdomain page #2  
- gamma.liber8.local.html – Subdomain page #3  
- delta.liber8.local.html – Subdomain page #4  
- omega.liber8.local.html – Subdomain page #5  

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge is about exploring web content and distinguishing real data from convincing fakes.
