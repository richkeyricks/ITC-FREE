import shutil
import os

def restore():
    p = os.getcwd()
    src_ico = os.path.join(p, 'assets', 'app_icon.ico')
    src_png = os.path.join(p, 'assets', 'app_icon.png')
    
    dest_dir = os.path.join(p, 'vercel_deploy', 'public')
    
    files_to_copy = [
        (src_ico, os.path.join(dest_dir, 'favicon.ico')),
        (src_png, os.path.join(dest_dir, 'apple-touch-icon.png')),
        (src_png, os.path.join(dest_dir, 'favicon-32x32.png')),
        (src_png, os.path.join(dest_dir, 'favicon-16x16.png')),
    ]
    
    for src, dest in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"Restored {os.path.basename(dest)} from {os.path.basename(src)}")
        else:
            print(f"Source not found: {src}")

if __name__ == "__main__":
    restore()
