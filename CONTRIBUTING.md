# 🤝 Contributing to `stemday_2025` (Admin-Only)

Welcome to the **CCRI CyberKnights STEM Day CTF Project!** 🎉  
This repository contains **all admin tools, source challenges, and packaging scripts** used to create the student VM.

> ⚠️ **Important:** Students only receive a **bundled version** with `ccri_ctf.pyz`.  
> Never commit generated artifacts (`.pyz`, JSONs, builds) to this repo.

---

## 🗂️ Repo vs Student VM

**Admin repo (this one):**

```
stemday_2025/
├── challenges/              # Exploration challenges
├── challenges_solo/         # Solo challenges
├── web_version/             # Student-facing portal
├── web_version_admin/       # Admin-only validation + templates
├── copy_ccri_ctf*.py        # Bundling scripts
├── generate_all_flags.py    # Flag + metadata generator
├── validate_all_flags.py    # Admin validator
├── ccri_ctf.pyz             # (⚠️ Generated only — don’t commit)
└── README.md / CONTRIBUTING.md
```

**Student VM (after bundling):**

```
Desktop/stemday_2025/
├── challenges/
├── challenges_solo/
├── web_version/
├── start_web_hub.py
├── stop_web_hub.py
├── Launch_CCRI_CTF_Hub.desktop
├── ccri_ctf.pyz   # 🔒 only runtime path
└── .ccri_ctf_root
```

---

## 🚀 Contributor Setup

1. **Install contributor environment:**

   ```bash
   curl -fsSL [https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/setup_contributor.py](https://raw.githubusercontent.com/CCRI-Cyberknights/stemday_2025/main/setup_contributor.py) | python3 -
   ```

2. **Clone repo:**

   ```bash
   git clone [https://github.com/CCRI-Cyberknights/stemday_2025.git](https://github.com/CCRI-Cyberknights/stemday_2025.git)
   cd stemday_2025
   ```

3. **Create a branch for your work:**

   ```bash
   git checkout -b feature/my-change
   ```

   ✅ For **CyberKnights org members**: branch directly inside this repo.  
   ❌ For **external contributors**: fork the repo first, then create your branch on the fork and open a PR back.

---

## 🛠 Workflow

1. **Generate fresh flags** (only if working on challenges):

   ```bash
   ./generate_all_flags.py
   ```

2. **Test locally**:

   * In **Exploration mode**: run `./copy_ccri_ctf.py` and launch hub.
   * In **Solo mode**: run `./copy_ccri_ctf_solo.py` and launch hub.
   * Validate with:

     ```bash
     ./validate_all_flags.py
     ```

3. **Commit cleanly**:

   ```bash
   git add .
   git commit -m "Add: new ROT13 challenge"  # example
   git push origin feature/my-change
   ```

4. **Open a Pull Request (PR)** → submit for review.  
   (Branches are preferred. Forks only if you lack write access.)

---

I've included a markdown cheatsheet here: [Markdown Cheatsheet](./markdown-cheat-sheet.md). See it on the GitHub webpage for examples, and open it as a text file to see the formatting code. To test out edits to the various README.md files, start the webserver in admin mode, load the page with the specific readme, and see how it renders. The readmes will change on a page refresh, but if you edit any actual HTML files, stop the server first and restart it to ensure the edits carry over.

---

## 🛡️ Rules & Best Practices

✅ **.pyz is the only runtime path for students** — no `.pyc` or raw source leaks  
✅ **Never commit:**
* `ccri_ctf.pyz`
* `validation_unlocks*.json`
* Take-home bundles or packaged folders

✅ Keep **admin-only** scripts inside `web_version_admin/`  
✅ Test both **Exploration + Solo** build flows before merging  
✅ Use **relative paths** (no `/home/username/...`) for portability  
✅ **PRs should explain:**
* Which challenges/scripts changed
* Whether flags were regenerated

---

## 🙌 Thanks for Contributing!

Every improvement helps make CCRI STEM Day a smoother experience for students. 🚩