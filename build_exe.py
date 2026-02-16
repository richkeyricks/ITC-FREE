# build_exe.py
import os
import subprocess
import shutil
import sys # Added import sys

def build():
    print("// Starting Optimized Build Process...")
    
    # 1. CLEANUP PREVIOUS BUILDS
    folders = ['build', 'dist']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"// Cleaned up {folder}/")

    # 2. RESOLVE ASSETS
    import customtkinter
    import CTkMessagebox
    ctk_path = os.path.dirname(customtkinter.__file__)
    msg_path = os.path.dirname(CTkMessagebox.__file__)
    
    # 3. DEFINE EXCLUSIONS (To reduce size)
    # Removing heavy libraries that aren't strictly required or are test/dev bloat
    exclusions = [
        "matplotlib.tests", "numpy.tests", "pandas.tests", 
        "IPython", "notebook", "jedi", "black", 
        "distutils", "lib2to3",
        "unittest", "pydoc", "email.test", "xmlrpc",
        "scipy" # EXCLUDED: Version conflict with Numpy 2.x
    ]
    
    # 4. UPX DETECTION
    # UPX (Ultimate Packer for eXecutables) significantly compresses the exe.
    # User should download UPX from https://upx.github.io/ and add to PATH or project root.
    upx_dir = "." # Assumes upx.exe might be in root if not in PATH
    
    # 5. PREPARE COMMAND
    cmd = [
        sys.executable, "-O", "-m", "PyInstaller", # Use current python interpreter (venv)
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--icon=assets/app_icon.ico",
        "--name=ITC_Plus_AI_Enterprise",
        f"--add-data={ctk_path};customtkinter/",
        f"--add-data={msg_path};CTkMessagebox/",
        "--add-data=assets;assets/",
        
        # --- FIXES FOR SQLITE3 & PYROGRAM ---
        "--hidden-import=sqlite3",
        "--hidden-import=_sqlite3", 
        "--hidden-import=pyrogram",
        "--hidden-import=pyrogram.storage",
        "--hidden-import=pyrogram.storage.sqlite_storage",
        "--hidden-import=pysqlite2",
        # --- CRITICAL HEAVY LIBS (Uncommented to fix crash) ---
        "--hidden-import=pandas",
        "--hidden-import=numpy", 
        "--hidden-import=PIL",
        "--hidden-import=mplfinance",
        "--paths=src", # CRITICAL: Ensure 'index.py' in src/ is found
        "--hidden-import=index", # Force include index module
        "--hidden-import=configs", # Force include configs package
        # ------------------------------------
    ]
    
    # Add exclusions to command
    for ex in exclusions:
        cmd.extend(["--exclude-module", ex])
        
    # Check for UPX
    if shutil.which("upx"):
        print("// UPX found! Applying high compression...")
        cmd.append("--upx-dir")
        cmd.append(os.getcwd()) # Just in case it's in the root
    else:
        print("// WARNING: UPX not found. Exe will be larger (~200MB+).")
        print("// Download from https://upx.github.io/ for 30-50% size reduction.")

    cmd.append("src/gui.py")
    
    print(f"// Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "="*50)
        print("Build Complete!")
        print("Location: dist/ITC_Plus_AI_Enterprise.exe")
        print("TIP: Use 7-Zip (Ultra/Solid) on the final .exe for sharing!")
        print("="*50)
    else:
        print("\n❌ Build Failed. Check logs above.")

if __name__ == "__main__":
    build()
