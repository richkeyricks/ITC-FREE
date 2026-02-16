import os
import sys
from PIL import Image, ImageOps

# Configuration
SOURCE_IMAGE_PATH = r"C:\Users\Richkeyrick\.gemini\antigravity\brain\2cbfcf1d-8f44-458c-ac50-8fcf6b3befbf\uploaded_media_1769656003097.png"
PROJECT_ROOT = r"c:\APLIKASI YANG DIBUAT\TELEGRAM MT5"

TARGETS = [
    # Web Assets
    {"path": r"vercel_deploy\public\favicon.ico", "sizes": [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)], "format": "ICO"},
    {"path": r"vercel_deploy\public\favicon-32x32.png", "size": (32, 32), "format": "PNG"},
    {"path": r"vercel_deploy\public\favicon-16x16.png", "size": (16, 16), "format": "PNG"},
    {"path": r"vercel_deploy\public\apple-touch-icon.png", "size": (180, 180), "format": "PNG"},
    {"path": r"vercel_deploy\public\android-chrome-192x192.png", "size": (192, 192), "format": "PNG"},
    {"path": r"vercel_deploy\public\android-chrome-512x512.png", "size": (512, 512), "format": "PNG"},
    
    # Desktop Assets
    {"path": r"assets\app_icon.ico", "sizes": [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)], "format": "ICO"},
]

def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    """
    Pad the image to make it square, preserving aspect ratio.
    This ensures the 'full view' of the logo is visible without cropping.
    """
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

def generate_icons():
    print(f"Loading source image from: {SOURCE_IMAGE_PATH}")
    try:
        if not os.path.exists(SOURCE_IMAGE_PATH):
            print(f"ERROR: Source image not found at {SOURCE_IMAGE_PATH}")
            return

        img = Image.open(SOURCE_IMAGE_PATH).convert("RGBA")
        
        # Ensure the base image is square first to handle non-square inputs gracefully
        # increasing canvas size to max dimension
        square_img = make_square(img)
        
        for target in TARGETS:
            full_path = os.path.join(PROJECT_ROOT, target["path"])
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            print(f"Generating: {target['path']}...")
            
            if target["format"] == "ICO":
                # For ICO, we can provide a list of sizes
                # We simply resize the square master image to each size
                # Windows ICOs often just need the image resized
                square_img.save(full_path, format="ICO", sizes=target["sizes"])
            else:
                # For PNGs, resize to specific target size
                target_size = target["size"]
                # High quality resampling
                resized = square_img.resize(target_size, Image.Resampling.LANCZOS)
                resized.save(full_path, format="PNG")
                
            print(f"  -> Saved to {full_path}")

        print("\nAll icons generated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_icons()
