🌐 Challenge #14 – Subdomain Sweep
-------------------------------------------

The Liber8 network uses multiple subdomains for internal operations. You’ve intercepted DNS information about five subdomains, each hosting a web page that proudly displays a “flag.” But only ONE of these flags is the **real agency flag**—the others are decoys.

Your mission:  
  1. Investigate each subdomain’s page.  
  2. Extract the flag text shown on the page.  
  3. Identify which flag is real based on the agency’s flag format.

🗂️ Files in this folder:
  • domains.txt            ← List of subdomains to check
  • explore_subdomains.sh  ← Guided helper script

💡 Hint: The real flag follows this format:  
       **CCRI-AAAA-1111**  
All other flags have a different prefix.

👩‍💻 Tip: Each subdomain page is a simple HTML file. You can use `cat`, `less`, or the helper script to explore them.

🚀 Start your sweep and find the correct flag!

