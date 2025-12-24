# 🌟 `stemday_2025` Project README (Admin-Only)

Welcome to the **CCRI CyberKnights STEM Day VM Project!** 🎉  
This repository powers the custom **Parrot Linux Capture The Flag (CTF)** used for STEM Day.

👥 **This repository is for CCRI CyberKnights club members only.** It contains source files, admin tools, and scripts used to **build and package** the student-facing VM.

---

## 🌀 Quick Setup (Admin Environment)

**Install dependencies & clone repo:**

```bash
curl -fsSL https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/setup_contributor.py | python3 -
git clone https://github.com/CCRI-Cyberknights/stemday_2025.git
cd stemday_2025
```

---

## 🗂️ Project Layout

```
stemday_2025/
├── challenges/                 # Exploration-mode challenges (with helpers)
├── challenges_solo/            # Solo-mode challenges (minimal hints)
├── web_version/                # Student-facing web portal
├── web_version_admin/          # Admin-only validation + templates
├── Launch_CCRI_CTF_Hub.desktop # Student launcher shortcut
├── copy_ccri_ctf.py            # Bundle → exploration+solo VM build
├── copy_ccri_ctf_solo.py       # Bundle → solo-only VM build
├── copy_takehome_ccri_ctf.py   # Bundle → for takehome repo
├── generate_all_flags.py       # Generate flags + JSON metadata
├── validate_all_flags.py       # Admin validator (exploration + solo)
├── start_web_hub.py / stop_*.py # Flask launcher
├── ccri_ctf.pyz                # 🔒 Student .pyz bundle (no .pyc needed)
└── README.md / CONTRIBUTING.md
```

---

## 🧭 Exploration vs Solo Modes

* **Exploration Mode** (`challenges/`): The "Guided" experience. Includes interactive helper scripts and detailed tutorials to teach core concepts.
* **Solo Mode** (`challenges_solo/`): The "Hard" mode. Features the same objectives and flags, but **no helpers or guided scripts**. Students must rely on their own CLI knowledge.

The **student launcher** auto-detects environment context:
* **Admin repo** (with `web_version_admin`): Prompts the user to choose which mode to launch.
* **Student VM** (no admin files, but has `ccri_ctf.pyz`): Launches directly into the bundled mode.

---

## 🚩 Flag Lifecycle

### 🔨 Generation
`generate_all_flags.py` creates:
* Real and fake flags inside challenge directories.
* Metadata for automated validation.
* `challenges.json` / `challenges_solo.json` for student-side checks.
* `validation_unlocks*.json` for admin-only validation.

### ✅ Validation
* **Admin**: Run `validate_all_flags.py` to simulate solving all challenges programmatically.
* **Students**: Flags are validated against `challenges.json` or `challenges_solo.json` within the VM.

---

## 🚀 Building Student VM Bundles

From the **admin repo**:

```bash
./generate_all_flags.py
./start_web_hub.py      # verify server is healthy
./validate_all_flags.py
```

Then choose the bundle type:

* **Exploration+Solo VM (classroom use):**
  ```bash
  ./copy_ccri_ctf.py
  ```
* **Solo-only VM (take-home / advanced):**
  ```bash
  ./copy_ccri_ctf_solo.py
  ```

**Build scripts automate the following:**
* Copying only required files for the specific bundle.
* Patching the desktop shortcut to point to the correct directory.
* Cleaning out admin-only content (e.g., `web_version_admin/`).
* Applying correct ownership and permissions for the `ccri_admin` user.

Students will only see:
```
Desktop/stemday_2025/
  ├── challenges/
  ├── challenges_solo/
  ├── web_version/
  ├── start_web_hub.py
  ├── stop_web_hub.py
  ├── Launch_CCRI_CTF_Hub.desktop
  ├── ccri_ctf.pyz
  └── .ccri_ctf_root
```

---

## 🙌 Notes for Contributors

* **Never commit .pyz or generated bundles to this repo.**
* **Test both Exploration and Solo builds before a release.**
* **.pyz is the only runtime path on student VMs** to ensure no bytecode mismatch.
* Admin-only JSONs (`validation_unlocks*.json`) **must stay in the admin repo only.**

---

## 📖 Contributing

If you want to contribute to this project, please read our [CONTRIBUTING.md](./CONTRIBUTING.md) guide. It explains branching, workflows, and best practices for making changes.