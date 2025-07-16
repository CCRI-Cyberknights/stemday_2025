# 🌟 `stemday2025` Admin Repository

Welcome to the **CCRI CyberKnights STEM Day CTF Project!** 🎉
This repository powers a custom **Parrot Linux Capture The Flag (CTF)** experience for high school students.

👥 **This repository is for CCRI CyberKnights club members only.**
It contains all of the **source files, admin tools, and scripts** used to build and maintain the student-facing version of the CTF.

> 🛑 **High school participants never see this repository or its contents.**
> They only interact with the pre-built *student version* deployed in their VM.

---

## 🗂️ Key Components

### 🖥️ **Admin Environment**

* `challenges/` – Source files for all interactive CTF challenges (editable by admins).
* `web_version_admin/` – Admin-only web portal, templates, and development tools.
* `web_version/` – Auto-generated **student-facing** web portal (no source files).
* `start_web_hub.sh` – Unified launcher for admin and student environments.
* `stop_web_hub.sh` – Cleanly stops the web server and simulated services.
* `build_web_version.sh` – Builds and obfuscates the student web portal, inside web_version_admin/create_website
* `copy_ccri_ctf.sh` – Copies the prepared CTF bundle to a student account Desktop.
* `.ccri_ctf_root` – Marker file for detecting the project root.

### 🎓 **Student Environment (what students see)**

* `challenges/` – Interactive CTF challenges.
* `web_version/` – Pre-built web portal (runs obfuscated server).
* `Launch CCRI CTF Hub.desktop` – Shortcut to start the web hub.

The **student version** is self-contained, with no developer tools or source files.

---

## 🚀 Preparing the Student VM

1. **Build the student web portal:**

   ```bash
   ./build_web_version.sh
   ```

   * Obfuscates all challenge flags.
   * Generates `web_version/` with only student-safe assets.

2. **Copy the bundle to the student account:**

   ```bash
   ./copy_ccri_ctf.sh
   ```

   * Copies `CCRI_CTF/` to the student Desktop.
   * Ensures correct ownership and permissions.

3. **Log in as the student** and verify:

   * ✅ The web hub launches correctly via `Launch CCRI CTF Hub.desktop`.
   * ✅ All challenges and scripts execute without admin privileges.

4. **Test the student experience.**

---

## 🔑 Key Scripts

| Script                 | Purpose                                                            |
| ---------------------- | ------------------------------------------------------------------ |
| `start_web_hub.sh`     | Unified launcher for admin (dev tools) and student (obfuscated).   |
| `stop_web_hub.sh`      | Stops the web hub and simulated services cleanly.                  |
| `build_web_version.sh` | Rebuilds and obfuscates the student portal.                        |
| `copy_ccri_ctf.sh`     | Copies the CTF folder to a student Desktop with fixed permissions. |

---

## 🛠 Admin Workflow (Quick Reference)

* 🔄 **Rebuild student portal:**

  ```bash
  ./build_web_version.sh
  ```

* 📂 **Copy to student account:**

  ```bash
  ./copy_ccri_ctf.sh
  ```

* 🚀 **Launch web hub (admin or student):**

  ```bash
  ./start_web_hub.sh
  ```

* 🛑 **Stop web hub and clean ports:**

  ```bash
  ./stop_web_hub.sh
  ```

---

## 🙌 Club Member Guidelines

✔️ Commit only admin/dev content to this repository.
✔️ Do **not** push compiled files (`*.pyc`, `__pycache__/`, etc.) or student builds (`web_version/`).
✔️ Test all new challenges and scripts before release.
✔️ Follow [CONTRIBUTING.md](CONTRIBUTING.md) for Git workflows and team collaboration.

---

## 🎓 Thank You!

This project exists thanks to the CCRI CyberKnights club’s dedication to creating an engaging and educational cybersecurity experience.

