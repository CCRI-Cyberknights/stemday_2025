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

## 📦 Install Dependencies (Required)

If you downloaded this CTF directly from GitHub (instead of using the USB stick or prebuilt ISO we provided), you’ll need to install some tools first.

Run this command in your VM’s terminal:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/CCRI-Cyberknights/stemday2025_home/main/setup_student.sh)
```

This will:
✅ Install all the tools needed for the challenges (like `hashcat`, `nmap`, and `steghide`).
✅ Place the CTF folder and desktop shortcut in the right location.

---

## 🗂️ Project Structure

Here’s what you’ll find on your VM’s Desktop after setup:

```
Desktop/
├── CCRI_CTF_Home/                  # Main CTF folder
│   ├── challenges/                 # All the hands-on CTF challenges
│   ├── web_version/                # The interactive hub website
│   ├── Launch CCRI CTF Hub.desktop # Shortcut to open the hub in a browser
└── (no admin scripts or hidden flags)
```

📝 **Note:**

* The `web_version/` folder contains the interactive CTF hub.
* Challenge flags are hidden in their respective folders — you can’t peek at them directly! 😄

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

If you’d like to pull the latest version of this CTF (if updates are released), run this in your VM’s terminal:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/CCRI-Cyberknights/stemday2025_home/main/setup_student.sh)
```

This will:
✅ Download the newest version of the student bundle into your **Downloads folder**.
✅ Replace old challenge files and hub content.

---

### 📄 **Move the Desktop Shortcut Back**

After running the update script:

1. Go to your **Downloads folder** and open the `CCRI_CTF_Home` folder.
2. Drag the **“Launch CCRI CTF Hub.desktop”** file back onto your Desktop.
3. Right-click the shortcut → **Properties → Permissions** → ✅ Check *“Allow this file to run as a program.”*

Now you’re ready to jump back in!

---

🎓 **Have fun, and good luck on your cyber journey!**
