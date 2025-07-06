# 🌱 stemday2025: STEM Day CTF VM (Admin)

Parrot Linux Home Edition VM designed for a **guided Capture The Flag (CTF)** experience for high school students.  

This repository is for **administrators and collaborators** creating and managing the CTF content. Students will receive a separate, simplified fork of this project that will be unguided to take home, baked into a USB stick with Parrot Home. 

---

## 🗂️ Folder Structure  

```
Desktop/
├── CCRI_CTF/               # Main CTF folder (shared with collaborators)
│   ├── challenges/         # All 15 interactive challenges
│   ├── web_version/        # Student-facing web portal (auto-generated)
│   ├── web_version_admin/  # Admin-only tools and templates
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── generate_scoreboard.py
├── capybara.jpg            # Placeholder/test images
└── squirrel.jpg
```

---

## 🚀 Admin Workflow  

### 🛠 Build the Student Web Hub
Run this from inside the VM to update `web_version/` after editing:  
```bash
cd ~/Desktop/CCRI_CTF/web_version_admin/admin_tools
python3 recode_flags.py
```
This will:  
✅ Obfuscate correct flags (Base64 + XOR).  
✅ Rebuild the student Flask server with secure settings.  
✅ Clear any stale files in `web_version/`.  

### 🧪 Test as Admin
Start the admin Flask server to preview challenges:  
```bash
cd ~/Desktop/CCRI_CTF/web_version_admin
python3 server.py
```
This version displays flags in plain text for easier debugging.

---

## 🛡️ Security Model  

- Students run in a **non-admin account (no sudo)**.  
- The VM auto-resets to a snapshot between sessions.  
- An **exit script** (desktop shortcut) requires the admin password to leave the loop.  
- Correct flags are **obfuscated** in the student web portal but visible to admins.  

---

## 🧑‍💻 Contributing  

Pull requests are welcome for:  
- New challenges.  
- UI improvements to the web portal.  
- Enhancements to admin tools (e.g., mass flag updates).  

See [CONTRIBUTING.md](CONTRIBUTING.md) for collaboration details.
