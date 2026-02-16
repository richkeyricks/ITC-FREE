from PIL import Image
import os

# --- CONFIGURATION ---
SOURCE_PATH = r"c:\APLIKASI YANG DIBUAT\TELEGRAM MT5\vercel_deploy\public\images\favicon\itc_master_icon.png"
DEST_DIR = r"c:\APLIKASI YANG DIBUAT\TELEGRAM MT5\vercel_deploy\public"

def generate_favicons():
    if not os.path.exists(SOURCE_PATH):
        print(f"❌ Error: Source file not found at {SOURCE_PATH}")
        return

    print(f"🔄 Loading master asset: {SOURCE_PATH}")
    try:
        img = Image.open(SOURCE_PATH)
    except Exception as e:
        print(f"❌ Error opening image: {e}")
        return

    # Ensure destination directory exists
    os.makedirs(DEST_DIR, exist_ok=True)

    # 1. Generate favicon.ico (Multi-resolution)
    ico_path = os.path.join(DEST_DIR, "favicon.ico")
    img.save(ico_path, format="ICO", sizes=[(32, 32), (16, 16)])
    print(f"✅ Generated: favicon.ico (16x16, 32x32) -> {ico_path}")

    # 2. Generate Standard PNGs
    targets = {
        "favicon-16x16.png": (16, 16),
        "favicon-32x32.png": (32, 32),
        "apple-touch-icon.png": (180, 180),
        "android-chrome-192x192.png": (192, 192),
        "android-chrome-512x512.png": (512, 512)
    }

    for filename, size in targets.items():
        try:
            # High-quality resampling
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            output_path = os.path.join(DEST_DIR, filename)
            resized_img.save(output_path)
            print(f"✅ Generated: {filename} ({size[0]}x{size[1]})")
        except Exception as e:
            print(f"❌ Failed to generate {filename}: {e}")

    print("\n🎉 Favicon generation complete!")

if __name__ == "__main__":
    generate_favicons()
