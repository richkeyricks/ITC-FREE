# ITC +AI Enterprise Executable Optimization Guide

To achieve the smallest possible file size for distribution, follow this three-step workflow.

## Step 1: Prepare UPX (PyInstaller Compression)
PyInstaller can compress the internal libraries if **UPX** is available.
1. Download UPX from [upx.github.io](https://upx.github.io/).
2. Extract `upx.exe`.
3. Place `upx.exe` directly into the project root folder (`c:\APLIKASI YANG DIBUAT\TELEGRAM MT5\`).
4. Run the build: `python build_exe.py`.

## Step 2: Build the Optimized App
The new `build_exe.py` is pre-configured with:
- **Python Optimization (`-O`)**: Removes unneeded debug code.
- **Aggressive Exclusions**: Excludes over 15+ heavy libraries (scipy, IPython, etc.) that aren't used but are often bundled by default.
- **UPX Support**: Automatically detects and uses `upx.exe` if you placed it in the folder.

## Step 3: 7-Zip Final Packaging
After the build completes, the file will be in the `dist/` folder.
1. Open **7-Zip GUI**.
2. Select `dist/ITC_Plus_AI_Enterprise.exe`.
3. Click **Add** to create an archive.
4. Set **Archive format**: `7z`.
5. Set **Compression level**: `Ultra`.
6. Set **Compression method**: `LZMA2`.
7. Set **Dictionary size**: `64MB` or higher.
8. Enable **Create solid archive**.

---
**Estimated Size Results:**
- Standard Build: ~350 MB
- Optimized Build (No UPX): ~220 MB
- Optimized Build (With UPX): ~140 MB
- Final 7z Archive (Ultra): **~45 - 60 MB**
