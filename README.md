# 🌟 `stemday2025` Project README (Org-Only)

Welcome to the **CCRI CyberKnights STEM Day VM Project!** 🎉
This repository powers a custom **Parrot Linux Capture The Flag (CTF)** experience for high school students.

👥 **This repo is for CCRI CyberKnights club members only.**

A **public “take-home” version** for students will be provided later in a separate repo without admin tools or guiding scripts.

---

## 🗂️ Project Structure

```
Desktop/
├── CCRI_CTF/                     # Main CTF folder (club development)
│   ├── challenges/               # All interactive CTF challenges
│   ├── web_version/              # Student-facing web portal (auto-generated)
│   ├── web_version_admin/        # Admin-only tools and templates
│   ├── README.md                  # Admin README (this file)
│   ├── CONTRIBUTING.md            # Collaboration guide for club members
│   ├── Launch CCRI CTF Hub.desktop # Shortcut to launch the student hub
│   ├── generate_scoreboard.py     # Admin utility scripts
│   ├── generate_qr_flags.sh       # Admin utility scripts
│   ├── generate_fake_authlog.py   # Admin utility scripts
│   ├── binary_flag.c              # Supporting code for binary challenge
│   ├── index_grid_obfuscated.html # Web portal prototype
│   ├── plan_overview.txt          # Project planning notes
│   ├── main_web_portal_idea.txt   # Web portal design notes
│   ├── capybara.jpg               # Assets and placeholder/test images
│   ├── squirrel.jpg               # Assets and placeholder/test images
└── (etc.)                         # Misc admin/dev tools
```

---

## 🚀 Workflow for Club Members

### 🛠 Editing Content

1. Clone the repo directly (no need to fork):

   ```bash
   git clone https://github.com/CCRI-Cyberknights/stemday2025.git
   cd stemday2025
   ```
2. Create a feature branch for your changes:

   ```bash
   git checkout -b feature/my-changes
   ```
3. Edit scripts, admin tools, or challenge folders.
4. Test your changes in the VM.

---

### 🔄 Submitting Changes

* Commit and push your branch:

  ```bash
  git add .
  git commit -m "Add new challenge or fix admin tool"
  git push origin feature/my-changes
  ```
* Open a Pull Request (PR) for review.
* Club admins will merge your branch into `main` if approved.

---

## 🛡️ Rules for Contributors

✅ Keep admin-only flags and tools **out of `web_version/`**
✅ Test all scripts from both the folder and the web portal
✅ Avoid absolute paths – use relative paths for portability
✅ Don’t commit generated `.pyc` files or student folders

---

## 📝 About the Public Repo

Students will later receive a **separate repo** with only the student-facing web portal and CTF challenges (no admin tools or walkthrough scripts).
This repo stays private to keep admin workflows and solution logic secure.

---

## 🙌 Thanks for contributing to CCRI’s STEM Day CTF!
