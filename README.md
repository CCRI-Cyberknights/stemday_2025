# 🌟 `stemday2025` Project README (Org-Only)

Welcome to the **CCRI CyberKnights STEM Day VM Project!** 🎉  
This repository powers a custom **Parrot Linux Capture The Flag (CTF)** experience for high school students.
To download that go here: https://www.parrotsec.org/download/

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
│   ├── README.md                 # This file
│   └── CONTRIBUTING.md           # Collaboration guide for club members
└── (etc.)                        # Misc admin/dev tools and assets
```

---

## 🚀 Placing the CTF Hub on the VM Desktop

To make the CTF experience accessible to students:  

1. Open the `CCRI_CTF/` folder on the VM.  
2. Locate the file named:  
   ```
   Launch CCRI CTF Hub.desktop
   ```
3. Drag and drop this shortcut onto the VM desktop.  
4. Right-click the desktop shortcut, choose **Properties → Permissions**, and ensure:  
   - ✅ “Allow this file to run as a program” is enabled.  

This shortcut launches the student web portal in a browser for easy access.  

---

## 🛠 Admin Workflow (Quick Reference)

* **Build student hub:**

  ```bash
  cd CCRI_CTF/web_version_admin/create_website
  python3 create_hub.py
  ```

  * Obfuscates flags and rebuilds the student web portal.

---

## 🙌 Club Member Guidelines

✅ Keep admin-only flags and tools **out of `web_version/`**  
✅ Test all scripts in both folder mode and web portal mode  
✅ Avoid absolute paths – use relative paths for portability  
✅ Don’t commit `.pyc` files or student-only builds  

---

## 🎓 Thanks for helping build CCRI CyberKnights STEM Day CTF!  

For more details on setting up Git and environment prerequisites, see [CONTRIBUTING.md](CONTRIBUTING.md).
