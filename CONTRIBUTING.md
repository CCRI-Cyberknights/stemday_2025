# 🌟 `stemday2025` Contributor Guide (Org-Only)

Welcome to the **CCRI CyberKnights STEM Day VM Project!** 🎉
This repository powers a custom **Parrot Linux Capture The Flag (CTF)** experience for high school students.

👥 **This repo is for CCRI CyberKnights club members only.**

A **public “take-home” version** for students will be hosted separately without admin tools or guiding scripts.

---

## 🗂️ Project Structure

```
Desktop/
├── CCRI_CTF/                     # Main CTF folder (club development)
│   ├── challenges/               # Interactive CTF challenges
│   ├── web_version/              # Student-facing web portal (auto-generated)
│   ├── web_version_admin/        # Admin-only tools and templates
│   ├── Launch CCRI CTF Hub.desktop # Shortcut to launch the student hub
│   ├── (various admin scripts)   # Tools for flag generation and testing
│   ├── README.md                  # This file
│   └── CONTRIBUTING.md            # Collaboration guide for club members
└── (etc.)                         # Misc admin/dev tools and assets
```

---

## 🚀 Joining the Repo

If you are a CCRI CyberKnights member and want to contribute:

1. Let **Tolgar (Corey)** know your GitHub username in Discord.
2. Corey will invite you to the **CCRI-Cyberknights GitHub organization**.
3. Accept the invite from your GitHub notifications or email.
4. Once you’re in, you’ll have collaborator access to this repo.

---

## 🧑‍💻 Setting Up Your Environment (Fresh VM)

### ✅ Install Git & Prerequisites

Run these commands inside your VM:

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv exiftool zbar-tools steghide hashcat unzip
```

### ⚙️ Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global credential.helper store
```

This saves your credentials for future pushes.

---

## 🛠 Workflow for Club Members

### 📥 Clone the Repo

```bash
git clone https://github.com/CCRI-Cyberknights/stemday2025.git
cd stemday2025
```

### 🌱 Create a Feature Branch

```bash
git checkout -b feature/my-changes
```

### 📝 Edit and Test

* Modify scripts, admin tools, or challenge folders.
* Test your changes both directly in folders **and** via the web portal.

### 💾 Commit and Push

```bash
git add .
git commit -m "Add new challenge or fix admin tool"
git push origin feature/my-changes
```

### 🔄 Open a Pull Request (PR)

1. Go to the repo on GitHub.
2. Click **“Compare & pull request.”**
3. Describe your changes.
4. Submit for review and merging.

---

## 🛡️ Rules for Contributors

✅ Keep admin-only flags and tools **out of `web_version/`**
✅ Test all scripts from both the folder and the web portal
✅ Use relative paths (avoid absolute paths) for portability
✅ Don’t commit generated `.pyc` files or student-only folders

---

## 📣 About the Public Repo

Students will later get a **separate public repo** with only the student-facing web portal and challenges (no admin scripts).
This repo stays **private** for club development and admin workflows.

---

## 🙌 Thanks for contributing to CCRI CyberKnights STEM Day CTF!

