# 🌟 `stemday_2025` Project README (Admin-Only)

Welcome to the **CCRI CyberKnights STEM Day VM Project!** 🎉
This repository powers the custom **Parrot Linux Capture The Flag (CTF)** used for STEM Day.

👥 **This repository is for CCRI CyberKnights club members only.** It contains source files, admin tools, and scripts used to **build and package** the student-facing VM.

---

## 🌀 Quick Setup (Admin Environment)

**Install dependencies & clone repo:**

```bash
curl -fsSL [https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/setup_contributor.py](https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/setup_contributor.py) | python3 -
git clone [https://github.com/CCRI-Cyberknights/stemday_2025.git](https://github.com/CCRI-Cyberknights/stemday_2025.git)
cd stemday_2025
```

---

## 📜 Script Reference

### 📦 Build & Deployment
These scripts package the CTF for different audiences.

| Script | Function |
| :--- | :--- |
| **`copy_ccri_ctf.py`** | **Standard STEM Day Build.** Copies the project from the Admin user (`ccri_admin`) to the Student user (`ccri_stem`) on the event VM. Includes **Exploration + Solo** modes. |
| **`copy_ccri_ctf_solo.py`** | **Advanced/Hard Mode Build.** Copies **ONLY** `challenges_solo` to the Student user. Removes all guided scripts, coach engines, and exploration content. |
| **`copy_takehome_ccri_ctf.py`** | **Public Repo Sync.** Exports the student-facing assets (challenges, web portal, engines) to the `stemday_2025_takehome` folder. Used to update the public GitHub repository. |

### ⚙️ Core Engines
The backend logic that powers the interactive elements.

| Script | Function |
| :--- | :--- |
| **`coach_core.py`** | The brain behind **Coach Mode**. Handles user input, hint logic, and interaction with the "Cyber Coach". |
| **`exploration_core.py`** | The engine for **Exploration Mode** scripts (`.explore.py`). Handles challenge state and guided tutorials. |
| **`worker_node.py`** | Helper module used by the core engines to execute sub-processes and validate flags safely. |

### 🚩 Flag Lifecycle & Admin
Tools for managing the challenge content.

| Script | Function |
| :--- | :--- |
| **`generate_all_flags.py`** | Generates real/fake flags, binaries, and metadata (`challenges.json`). Run this first! |
| **`validate_all_flags.py`** | Automated testing. Simulates a user solving every challenge to ensure flags work correctly. |
| **`reset_environment.py`** | **Cleanup.** Deletes all generated artifacts (binaries, logs, flags) to return the repo to a clean state. |
| **`setup_contributor.py`** | Installs Python dependencies (`flask`, `termcolor`, etc.) needed to develop on this repo. |

### 🌐 Web Interface
| Script | Function |
| :--- | :--- |
| **`start_web_hub.py`** | Launches the offline Flask web server (The "Hub" where students verify flags). |
| **`stop_web_hub.py`** | Safely shuts down the web server background process. |

---

## 🚀 Workflow for Contributors

1.  **Generate Assets:**
    ```bash
    ./generate_all_flags.py
    ```
2.  **Test Locally:**
    * Start the hub: `./start_web_hub.py`
    * Run the validator: `./validate_all_flags.py`
3.  **Build (Optional Test):**
    * Simulate a student install: `./copy_ccri_ctf.py`
4.  **Clean Up:**
    * **ALWAYS** run this before committing:
    ```bash
    ./reset_environment.py
    ```

---

## 🙌 Notes

* **Never commit .pyz or generated bundles.**
* **.pyz is the only runtime path for students** (containing the answers) to ensure no source leaks.
* Admin-only JSONs (`validation_unlocks*.json`) **must stay in the admin repo only.**

---

## 📖 Contributing

If you want to contribute to this project, please read our [CONTRIBUTING.md](./CONTRIBUTING.md) guide. It explains branching, workflows, and best practices for making changes.