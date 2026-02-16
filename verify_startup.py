import os
import sys

# Add src to path
sys.path.append(os.path.abspath("src"))

try:
    from gui import STCApp
    import customtkinter as ctk
    
    # Initialize app to check for immediate crashes
    ctx = STCApp()
    print("SUCCESS: STCApp initialized without crash.")
    ctx.destroy()
    sys.exit(0)
except Exception as e:
    print(f"FAILED: Application failed to initialize. Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
