# GitHub Release & Download Guide

To make your **71.3 MB ZIP** easily downloadable from GitHub (instead of just downloading the source code), you should create a **GitHub Release**.

## 1. Create a GitHub Release
Don't just upload the ZIP to the file list; follow these steps:
1. Go to your repository [richkeyricks/ITC-FREE](https://github.com/richkeyricks/ITC-FREE).
2. On the right-side sidebar, look for **Releases** and click **Create a new release** (or "Tags" -> "Releases").
3. **Choose a tag**: Type `v1.0.1` and click "Create new tag".
4. **Release title**: `ITC +AI Enterprise v1.0.1`.
5. **Describe this release**: You can copy-paste:
   ```markdown
   ## 🚀 Official Enterprise Release (Optimized)
   - **Size**: 71.3 MB (Standalone EXE)
   - **Fixes**: Registration flow crash resolved.
   - **Optimization**: Sub-75MB reached with aggressive exclusion.
   ```
6. **Attach binaries**: Look for the "Attach binaries by dropping them here" box.
7. **Drag and drop** your `dist/ITC_Plus_AI_Enterprise.zip` into that box.
8. Click **Publish release**.

---

## 2. Add "Download" Button to README
To make it look professional, add this to the very top of your `README.md`:

```markdown
# ITC +AI Enterprise 📈

[![Download Zip](https://img.shields.io/badge/Download-Release_ZIP-blue?style=for-the-badge&logo=github)](https://github.com/richkeyricks/ITC-FREE/releases/latest)

---
```

## 3. Difference between "Download ZIP" and "Release"
- **Download ZIP (in your picture)**: Only downloads the `.py` source code. It **will not run** for normal users.
- **GitHub Release (Recommended)**: Downloads your compiled `.exe` (inside the ZIP), which works instantly without Python installed.

---
**Status**: Once you upload to Releases, your users can download the professional binary directly!
