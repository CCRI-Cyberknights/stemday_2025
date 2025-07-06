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

## 🚀 Contributing as a Club Member

This repo is private for CCRI CyberKnights members. To contribute:

1. Let **Tolgar (Corey)** know your GitHub username in Discord.
2. Accept the GitHub invitation.
3. Clone the repo and start working:

   ```bash
   git clone https://github.com/CCRI-Cyberknights/stemday2025.git
   cd stemday2025
   ```
4. Create a feature branch:

   ```bash
   git checkout -b feature/my-changes
   ```
5. Make and test your changes.
6. Push and open a Pull Request (PR) for review.

---

## 🛠 Admin Workflow (Quick Reference)

* **Build student hub:**

  ```bash
  cd CCRI_CTF/web_version_admin/admin_tools
  python3 recode_flags.py
  ```

  * Obfuscates flags and rebuilds the student web portal.

* **Test web portal (admin mode):**

  ```bash
  cd CCRI_CTF/web_version_admin
  python3 server.py
  ```

---

## 🛡️ Club Member Guidelines

✅ Keep admin-only flags and tools **out of `web_version/`**
✅ Test all scripts in both folder mode and web portal mode
✅ Avoid absolute paths – use relative paths for portability
✅ Don’t commit `.pyc` files or student-only builds

---

## 🙌 Thanks for helping build CCRI CyberKnights STEM Day CTF!

For more details on setting up Git and environment prerequisites, see [CONTRIBUTING.md](CONTRIBUTING.md).
