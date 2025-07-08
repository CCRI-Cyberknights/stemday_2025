🧠 Challenge #16 – Hex Flag Hunter
-------------------------------------

💼 Situation:
We’ve intercepted a suspicious binary file named `hex_flag.bin` from a hacker’s stash. It’s too small to be a real program, but we suspect it contains a **hidden flag** embedded somewhere in the data.

🎯 Your Mission:
Use your forensic skills to scan the binary and locate the correct flag.

📖 HINTS:
- The flag is **hidden as ASCII text** inside the binary. It follows this format:
  `CCRI-AAAA-1111`
- There are **five candidate flags** scattered throughout the file, but only ONE is correct.
- Some hex editors can display both hex and ASCII at the same time.

🛠 Tools at Your Disposal:
- **hexedit** → Interactive hex editor (easiest for scrolling/searching).
- **xxd** → Dumps the file as hex + ASCII.
- **strings** → Might help, but not all candidates will show up cleanly.

---

📂 Files Provided:
- `hex_flag.bin` – Suspicious binary to investigate.
- `inspect_binary.sh` – Helper script to launch hex editors.

✅ Once you find the correct flag, paste it into the **flag verifier** in the student hub to confirm your success.

