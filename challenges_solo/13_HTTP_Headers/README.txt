# 📡 Challenge 13: HTTP Headers Mystery

Liber8 operatives have been exchanging secret messages through HTTP servers.  
You’ve intercepted five HTTP response files, but only ONE contains the real agency flag. The others are decoys designed to mislead intruders.

---

## 🎯 Your Mission

1. Investigate each HTTP response carefully.  
2. Look for a hidden X-Flag: header in the response.  
3. Identify the correct flag in this format:  
   CCRI-AAAA-1111  

---

## 🛠 Tools You Might Use

- less – View and scroll through each HTTP response file.  
- grep – Search for specific headers (e.g., `grep "X-Flag:" response_1.txt`).  
- cat – Quickly display a file’s contents.  

---

## 📝 Challenge Instructions

1. Open each response file one by one and review the headers.  
2. Search for the X-Flag: header that contains a flag-like string.  
3. Verify that the flag matches the agency’s official format. Fake flags will use different prefixes.  

Hint: Only one flag starts with CCRI-. All others are impostors.

Note: If you find the correct flag, save it manually:

echo "CCRI-AAAA-1111" > flag.txt

---

## 🗂️ Files in this folder

- response_1.txt – Captured HTTP response #1  
- response_2.txt – Captured HTTP response #2  
- response_3.txt – Captured HTTP response #3  
- response_4.txt – Captured HTTP response #4  
- response_5.txt – Captured HTTP response #5  

---

## 🏁 Flag Format

When you find the flag, it will look like this:

CCRI-AAAA-1111

Replace the AAAA and numbers with the real code you uncover.

---

This challenge teaches you how to analyze HTTP headers like a security analyst scanning for hidden messages.
