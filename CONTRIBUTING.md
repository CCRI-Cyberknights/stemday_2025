# 🚀 `stemday2025` GitHub Contributor Guide

Welcome to the **STEM Day VM project**! This repo powers a custom-built **Parrot Linux CTF experience** for high school students.

---

## 📦 Project Overview

**STEM Day VM**  
A locked-down, game-like Linux environment for cybersecurity education.

- 🐦 **Parrot Linux Home Edition**
- 🔒 No `sudo` access for students
- 🖥️ All interaction happens in a folder on the Desktop
- 🎮 Each script simulates a security scenario (with prompts and/or visuals)
- 🏁 Scripts output a **flag selection** screen and export the selected flag to a text file
- 🔍 Students paste the flag into an offline HTML **flag verifier**
  - Correct flags are **obfuscated via Base64 + XOR**
- ♻️ A snapshot resets the VM between groups
- 🔐 Exiting the VM loop requires the **admin password**, as all GUI controls are disabled and the VirtualBox host key is custom-set

---

## 🧑‍💻 How to Collaborate

You’ve been invited to contribute to the repo:  
👉 [https://github.com/Tolgar28/stemday2025](https://github.com/Tolgar28/stemday2025)

---

## 🔐 Step 1: Create a GitHub Token (No password login allowed)

1. Go to: [https://github.com/settings/tokens?type=beta](https://github.com/settings/tokens?type=beta)
2. Click **"Generate new token"**
3. Name: `stemday token`
4. Expiration: Choose any (e.g., 90 days)
5. Repository access: Select **“Only select repositories”** → check `stemday2025`
6. Permissions:
   - ✅ Contents: Read and write
7. Click **Generate token**
8. 📋 Copy and store it safely — you’ll paste it during your first push

---

## 💻 Step 2: Clone the Repo

Open a terminal (e.g. in the VM):

```bash
git clone https://github.com/Tolgar28/stemday2025.git
cd stemday2025
```

> When asked:
> - **Username** → your GitHub username  
> - **Password** → paste your GitHub token

---

## 💾 Step 3: Save Your Token (Optional)

```bash
git config --global credential.helper store
```

This saves your token locally so you don’t need to retype it.

---

## ✏️ Step 4: Make Edits and Push Changes

```bash
# Make edits to scripts or challenge folders...

git add .
git commit -m "Update to flag logic or UI text"
git push origin main
```

---

## ⚠️ Troubleshooting Pushes

### 🛑 Error: "Updates were rejected..."
If you see:
```
Updates were rejected because the remote contains work that you do not have locally.
```
Run this:
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

---

## 🔁 Optional: Pull Requests Instead of Direct Push

If you'd prefer to review changes before merging:

1. Fork the repo to your own GitHub account
2. Clone your fork
3. Make your changes
4. Push to your fork
5. On GitHub, open a **Pull Request** back to `Tolgar28/stemday2025`

---
