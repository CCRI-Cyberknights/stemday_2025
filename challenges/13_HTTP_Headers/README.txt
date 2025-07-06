📡 Challenge #13 – HTTP Headers Mystery
-------------------------------------------

Liber8 operatives have been communicating through HTTP servers. You’ve intercepted five HTTP responses, but only ONE of them contains the **real agency flag**. The others are clever decoys designed to throw you off.

Your mission:  
  1. Investigate each HTTP response file carefully.  
  2. Look for an `X-Flag:` header buried in the response.  
  3. Determine which flag is correct based on the agency’s known format.

🗂️ Files in this folder:
  • response_1.txt    ← Captured HTTP response #1
  • response_2.txt    ← Captured HTTP response #2
  • response_3.txt    ← Captured HTTP response #3
  • response_4.txt    ← Captured HTTP response #4
  • response_5.txt    ← Captured HTTP response #5
  • explore_responses.sh ← Guided helper script

💡 Hint: The agency flag format is:  
       **CCRI-AAAA-1111**  
All other flags have a different prefix.

👩‍💻 Tip: Use `cat`, `less`, or `grep` in the helper script to examine these files.  
👉 *If using `less`, press **q** to quit and return to the menu.*

🚀 Let’s uncover the correct flag!

