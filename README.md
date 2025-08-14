# 🌟 `stemday_2025` Project README (Admin-Only)

Welcome to the **CCRI CyberKnights STEM Day VM Project!** 🎉
This repository powers a custom **Parrot Linux Capture The Flag (CTF)** experience designed for high school students.

👥 **This repository is for CCRI CyberKnights club members only.**
It contains source files, admin tools, and scripts used to **build and maintain** the student-facing version of the CTF.

To download Parrot Linux for testing: [https://www.parrotsec.org/download/](https://www.parrotsec.org/download/)
The student VM uses the **Home Edition**, but testing on the **Security Edition** is fine.

---

## 🌀 Quick Setup (Admin Environment → Then Clone)

**Step 1 — Install tools (non-interactive):**

```bash
curl -fsSL https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/setup_contributor.py | python3 -
```

> This installs dependencies and *may* skip Git prompts if stdin isn’t a TTY (which is normal for `curl | python`). If you want to set Git identity non-interactively:

```bash
GIT_NAME="Your Name" GIT_EMAIL="you@example.com" \
  curl -fsSL https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/setup_contributor.py | python3 -
```

**Step 2 — Clone this repository:**

```bash
git clone https://github.com/CCRI-Cyberknights/stemday_2025.git
cd stemday_2025
```

**Optional one-liner (do both in one shot):**

```bash
curl -fsSL https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/setup_contributor.py | python3 - && \
git clone https://github.com/CCRI-Cyberknights/stemday_2025.git && \
cd stemday_2025
```

---

## 🗂️ Project Structure (Admin Repo)

```
Desktop/
├── stemday_2025/
│   ├── challenges/                 # Guided-mode challenges (with helper scripts)
│   ├── challenges_solo/            # Solo-mode challenges (minimal hints)
│   ├── web_version/                # Student-facing web portal (generated)
│   ├── web_version_admin/          # Admin-only tools and templates
│   ├── Launch CCRI CTF Hub.desktop # Student launcher shortcut
│   ├── generate_all_flags.py       # 🔐 Generate real/fake flags + metadata
│   ├── validate_all_flags.py       # ✅ Simulate solving to verify challenges
│   ├── copy_ccri_ctf.py            # 📦 Copies student-ready files to VM desktop
│   ├── README.md                   # This file
│   └── CONTRIBUTING.md             # Contribution guidelines
```

---

## 🧭 Guided vs Solo Modes

* **Guided Mode** (`challenges/`): interactive helper scripts walk students through.
* **Solo Mode** (`challenges_solo/`): same objectives, fewer hints.

The **web portal** in `web_version/` lets students choose a track.

---

## 🚩 Flag Generation & Validation

### 🔨 Flag Generation

`generate_all_flags.py` will:

* Create **real** flags and plant **fake** ones.
* Populate `challenges/` and `challenges_solo/`.
* Write metadata to:

  * `web_version_admin/validation_unlocks.json` (guided)
  * `web_version_admin/validation_unlocks_solo.json` (solo)
  * `web_version_admin/challenges.json` and `.../challenges_solo.json` (web validation)

### ✅ Validation Layers

1. **Admin validator** — `validate_all_flags.py`
   Simulates the student workflow to ensure each challenge and its embed/logic work.
   Solo challenges reuse hidden validation logic living in guided helpers.

2. **Student web portal**
   `server.py` checks submissions against the generated JSON and updates the UI.

> ⚠️ Start the Flask server before validating—**Challenge #17 (Nmap Scan)** expects simulated open ports.

---

## 🚀 Preparing the Student VM

From the repo root (admin box):

```bash
./generate_all_flags.py
./start_web_hub.py
./validate_all_flags.py
./web_version_admin/create_website/build_web_version.py
./copy_ccri_ctf.py
```

On the **student VM desktop**:

* Right-click `Launch CCRI CTF Hub.desktop` → **Properties → Permissions**
* Enable **“Allow this file to run as a program.”**

---

## 🔧 Troubleshooting Git after curl

If you skipped Git prompts during the setup one-liner, set identity now:

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global credential.helper store
```

Then clone:

```bash
git clone https://github.com/CCRI-Cyberknights/stemday_2025.git
cd stemday_2025
```

---

## 🙌 Club Member Guidelines

* Keep admin-only files out of student deliverables
* Test both guided and solo tracks
* Use relative paths
* Don’t commit `.pyc` or generated bundles (see `.gitignore`)

---

## 🎓 Thanks for helping build CCRI CyberKnights STEM Day CTF!

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution details.
