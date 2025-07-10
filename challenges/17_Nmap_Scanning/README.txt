🛰️ Challenge 17: Nmap Scan Puzzle
==================================

Several simulated services are running locally on this system.  
Your mission is to uncover the **REAL flag** hidden among them.

🎯 **Your Mission:**  
1️⃣ Run the provided helper script to scan for open ports in the range **8000–8100**.  
2️⃣ Explore the discovered services and inspect their responses.  
3️⃣ Identify the **one true flag** and submit it to the scoreboard.  

⚠️ **Not every open port contains a flag:**  
- Some return random junk text (e.g., error pages, developer APIs).  
- Four ports return **decoy flags** with slightly wrong formats.  
- Only **one port** contains the real flag in this format:  

   ✅ **CCRI-AAAA-1111**

🛠️ **Start Here:**  
Run the guided script:  

./scan\_services.sh

The script will:  
- Use **nmap** to scan for open ports.  
- Let you explore each service one by one.  
- Save interesting responses to a file for later review.  

💡 **Tip:** Pay close attention to the format of each flag. Only one matches the official CCRI style.  

📂 **Files Provided:**  
• `scan_services.sh` → Guided scanning and exploration tool  

---

🚀 **Objective:** Find the correct flag and paste it into the scoreboard.
