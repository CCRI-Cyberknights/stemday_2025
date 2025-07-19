# 🌟 CCRI CyberKnights STEM Day CTF – Take Home Edition

Welcome to the **CCRI CyberKnights STEM Day Virtual Machine!** 🎉
This repository contains a custom **Parrot Linux Capture The Flag (CTF)** experience designed for high school students.

You’re running this after setting up your **Parrot OS Home VM in VirtualBox**. This CTF is your chance to explore cybersecurity concepts in a fun, hands-on way.

---

## 🚀 What is this?

This is a self-contained cybersecurity challenge environment:

* 🛠 **No internet required** once it’s installed — everything runs locally in your VM.
* 🧩 Solve puzzles, explore tools, and uncover hidden flags.
* 💡 Each challenge teaches you **how tools work**, **why they’re used**, and **what’s happening under the hood**.

This version is built for **students**, with all admin/developer-only tools removed.

---

## 📥 Setting Up the CTF

If you downloaded this CTF directly from GitHub (or are looking at it online), follow these steps to set it up:

### ✅ 1. Install Required Tools

Run this command in your VM’s terminal to install everything you’ll need for the challenges:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/CCRI-Cyberknights/stemday2025_takehome/main/setup_student.sh)
```

This will:
✅ Install all the tools needed for the challenges (like `hashcat`, `nmap`, and `steghide`).

---

### ✅ 2. Download the CTF Folder

After installing the tools, download this CTF repository.

**Option A: Download ZIP**

1. Click the green **“Code”** button above → **“Download ZIP”**.
2. Extract the ZIP file to your **Downloads folder**.

**Option B: Clone with Git**
If you’re comfortable with Git, run:

```bash
git clone https://github.com/CCRI-Cyberknights/stemday2025_takehome.git
```

---

### ✅ 3. Move the CTF Folder to Your Desktop

1. Move the extracted folder (`stemday2025_takehome/`) to your **Desktop**.

2. Inside that folder, you’ll find:

   * **challenges/** – The hands-on CTF challenges.
   * **web\_version/** – The interactive CTF hub.
   * **Launch CCRI CTF Hub.desktop** – Shortcut to open the hub in a browser.

3. Drag the **“Launch CCRI CTF Hub.desktop”** file to your Desktop.

4. Right-click the shortcut → **Properties → Permissions** → ✅ Check *“Allow this file to run as a program.”*

---

## 🎯 How to Start

1. Double-click **“Launch CCRI CTF Hub”** on the Desktop.
2. The CTF hub will open in your browser.
3. Pick a challenge from the grid and dive in!

Each challenge includes:
✅ A walkthrough of the tools involved.
✅ An explanation of how and why they’re used.
✅ A goal to uncover a hidden flag.

---

## 🌐 Updating Your CTF (Optional)

If updates are released, you can re-download the latest version of this repository and repeat **steps 2–3** above.

---

🎓 **Have fun, and good luck on your cyber journey!**
