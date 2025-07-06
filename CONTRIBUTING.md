# 🚀 `stemday2025` Contributor Guide

Welcome to the **STEM Day VM Project**! This repo powers a custom-built **Parrot Linux CTF experience** for high school students.  

We’re building a **gamified cybersecurity “gym”** where students solve challenges inside a locked-down Linux VM.  

---

## 📦 Project Overview

- 🐦 **Parrot Linux Home Edition** base  
- 🔒 No `sudo` access for students  
- 🖥️ All interaction happens in a Desktop folder with scripts, data files, and a web portal  
- 🎮 Each script simulates a security scenario (with prompts and visuals)  
- 🏁 Students paste flags into an offline HTML **flag tracker**  
- 🔐 Admin-only features are separated into a `web_version_admin` folder  
- ♻️ VM resets to a snapshot between student groups  
- 🔓 Exiting the loop requires an admin password  

---

## 🧑‍💻 How to Contribute  

This repo is owned by **CCRI CyberKnights**, and collaborators don’t have direct commit rights to `main`. To contribute:  

✅ **Fork the repo** → make changes → submit a Pull Request (PR).  

This keeps `main` clean and lets us review edits before merging.  

---

### 📝 Step 1: Fork the Repo

1. Go to: [https://github.com/CCRI-Cyberknights/stemday2025](https://github.com/CCRI-Cyberknights/stemday2025)  
2. Click the **“Fork”** button (top right) to copy the repo into your GitHub account  

---

### 💻 Step 2: Clone Your Fork

Open a terminal:  

\`\`\`bash
git clone https://github.com/<your-username>/stemday2025.git
cd stemday2025
\`\`\`

---

### 🌱 Step 3: Create a Branch

Make a new branch for your changes:  

\`\`\`bash
git checkout -b my-cool-update
\`\`\`

---

### ✏️ Step 4: Make Your Changes

- Edit scripts in `challenges/` or admin tools in `web_version_admin/`  
- Keep in mind: students will only see the `web_version` folder  

---

### 💾 Step 5: Commit and Push

\`\`\`bash
git add .
git commit -m "Describe what you changed"
git push origin my-cool-update
\`\`\`

---

### 🔄 Step 6: Open a Pull Request (PR)

1. Go to your fork on GitHub  
2. Click **“Compare & pull request”**  
3. Describe what you changed  
4. Submit the PR  

We’ll review and merge it if everything looks good ✅  

---

## ⚠️ Guidelines

✅ Keep all scripts runnable directly from the VM **and** the web portal  
✅ Don’t hardcode absolute paths – use relative paths  
✅ Avoid exposing admin-only flags in plaintext in student-facing folders  
✅ Test your changes in a fresh clone if possible  

---

## 🚨 Direct Commits Are Disabled  

Only core maintainers (like the admin account) can push directly to `main`. All other edits must come in via Pull Requests.  
