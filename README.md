Got it 👍 — your current README is written as **admin-only instructions**. Since you now have **two copy scripts** (`copy_ccri_ctf.py` and `copy_ccri_ctf_solo.py`) and `.pyz` packaging, it’d help to clarify what’s for admins vs what ends up in the student VM.

Here’s a suggested edit (lean and precise, with **explanations where needed**):

---

# 🌟 `stemday_2025` Project README (Admin-Only)

Welcome to the **CCRI CyberKnights STEM Day VM Project!** 🎉
This repository powers the custom **Parrot Linux Capture The Flag (CTF)** used for STEM Day.

👥 **This repository is for CCRI CyberKnights club members only.**
It contains source files, admin tools, and scripts used to **build and package** the student-facing VM.

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
├── challenges/                 # Guided-mode challenges (with helpers)
├── challenges_solo/            # Solo-mode challenges (minimal hints)
├── web_version/                # Student-facing web portal
├── web_version_admin/          # Admin-only validation + templates
├── Launch_CCRI_CTF_Hub.desktop # Student launcher shortcut
├── copy_ccri_ctf.py            # Bundle → guided+solo VM build
├── copy_ccri_ctf_solo.py       # Bundle → solo-only VM build
├── copy_takehome_ccri_ctf.py   # Bundle → for takehome repo
├── generate_all_flags.py       # Generate flags + JSON metadata
├── validate_all_flags.py       # Admin validator (guided + solo)
├── start_web_hub.py / stop_*.py # Flask launcher
├── ccri_ctf.pyz                # 🔒 Student .pyz bundle (no .pyc needed)
└── README.md / CONTRIBUTING.md
```

---

## 🧭 Guided vs Solo Modes

* **Guided Mode** (`challenges/`): interactive helper scripts available.
* **Solo Mode** (`challenges_solo/`): same objectives, **no helpers**.

The **student launcher** auto-detects if it’s running:

* Admin repo (with `web_version_admin`) → asks which mode.
* Student VM (no admin files, but has `ccri_ctf.pyz`) → launches directly, no prompt.

---

## 🚩 Flag Lifecycle

### 🔨 Generation

`generate_all_flags.py` creates:

* Real + fake flags inside challenges
* Metadata for validation
* `challenges.json` / `challenges_solo.json` (student checks)
* `validation_unlocks*.json` (admin checks only)

### ✅ Validation

* **Admin**: run `validate_all_flags.py` → simulates solving all challenges
* **Students**: flags validated only against `challenges.json` / `...solo.json` inside the VM

---

## 🚀 Building Student VM Bundles

From the **admin repo**:

```bash
./generate_all_flags.py
./start_web_hub.py      # make sure server is healthy
./validate_all_flags.py
```

Then choose the bundle type:

* **Guided+Solo VM (classroom use):**

  ```bash
  ./copy_ccri_ctf.py
  ```

* **Solo-only VM (take-home / advanced):**

  ```bash
  ./copy_ccri_ctf_solo.py or ./copy_takehome_ccri_ctf.py
  ```

Both scripts:

* Copy only the needed files
* Patch the desktop shortcut to point at the right folder
* Clean out admin-only content (`web_version_admin/`, guided HTML, etc.)
* Apply correct ownership/permissions for `ccri_admin`

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

* **Never commit .pyz or generated bundles to this repo**
* **Test both guided and solo builds before release**
* **.pyz is the only runtime path on student VMs** — ensures no bytecode mismatch
* Admin-only JSONs (`validation_unlocks*.json`) **stay in admin repo only**
