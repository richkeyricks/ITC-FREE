
import os

file_path = r"c:\APLIKASI YANG DIBUAT\TELEGRAM MT5\web\index.html"

with open(file_path, 'rb') as f:
    content = f.read()

# Define replacements (bytes -> bytes)
replacements = {
    # General Fixes
    b'\xc3\xa2\xe2\x80\x9e\xc2\xa2': b'\xe2\x84\xa2', # â„¢ -> ™ (UTF-8 bytes for ™ is E2 84 A2)
    # Wait, let's look at what specific bytes map to the mojibake.
    # â„¢ interpreted as Windows-1252:
    # â = E2
    # „ = 84
    # ¢ = A2
    # So the bytes in the file likely ARE E2 84 A2.
    # But when viewed as Windows-1252, they show â„¢.
    # So the file IS ALREADY VALID UTF-8. The user's browser is just interpreting it as Windows-1252?
    # NO. The user said "tulisan aneh" and showed screenshot. The screenshot shows â„¢.
    # This means the browser IS rendering â„¢.
    # This implies the bytes in the file are actually the UTF-8 bytes for â, „, ¢.
    # UTF-8 for â = C3 A2
    # UTF-8 for „ = E2 80 9E
    # UTF-8 for ¢ = C2 A2
    # So the file contains C3 A2 E2 80 9E C2 A2.
    # And we want it to be E2 84 A2 (™).
    
    # Let's verify this hypothesis.
    # If the file has C3 A2 E2 80 9E C2 A2, and we replace it with E2 84 A2, it fixes it.
    
    # Mappings based on "Double UTF-8 encoding":
    # 1. ™ (E2 84 A2) -> â„¢ (C3 A2 E2 80 9E C2 A2)
    # 2. ⚡ (E2 9A A1) -> âš¡ (C3 A2 C5 A1 C2 A1)
    # 3. ★ (E2 98 85) -> â˜… (C3 A2 CB 9C E2 80 A6)  Wait, â˜… is C3 A2 CB 9C E2 80 A6?
    #    Let's check:
    #    â (E2) -> C3 A2
    #    ˜ (98) -> CB 9C  (SMALL TILDE) ? No. 98 in Windows-1252 is ˜ (tilde).
    #    ★ (E2 98 85). 
    #    E2 -> â (C3 A2)
    #    98 -> ˜ (CB 9C) ? No, 0x98 in 1252 is ˜. UTF-8 for ˜ (U+02DC) is CB 9C. Correct.
    #    85 -> … (E2 80 A6) ? 0x85 in 1252 is …. UTF-8 for … (U+2026) is E2 80 A6. Correct.
    #    So E2 98 85 becomes C3 A2 CB 9C E2 80 A6.
    
    # 4. 🦅 (F0 9F A6 85)
    #    F0 -> ð (C3 B0)
    #    9F -> Ÿ (C5 B8)
    #    A6 -> ¦ (C2 A6)
    #    85 -> … (E2 80 A6)
    #    Target: C3 B0 C5 B8 C2 A6 E2 80 A6 -> F0 9F A6 85
    
    # 5. 🐋 (F0 9F 90 8B)
    #    F0 -> ð (C3 B0)
    #    9F -> Ÿ (C5 B8)
    #    90 ->   (C2 90) ? 0x90 in 1252 is undefined? Or maybe it is handled as is?
    #    Let's check the previous view_file output.
    #    It showed "ðŸ ‹".
    #    ð (C3 B0)
    #    Ÿ (C5 B8)
    #      (C2 90) - This is mostly likely the invisible control char.
    #    ‹ (E2 80 93)? No. 0x8B in 1252 is ‹ (Single Left-Pointing Angle Quotation Mark).
    #    UTF-8 for ‹ (U+2039) is E2 80 B9.
    #    Wait, 8B -> ‹.
    #    So expected seq: C3 B0 C5 B8 C2 90 E2 80 B9.
    
    # REPLACEMENT STRATEGY:
    # Since I already identified the characters visually in view_file,
    # I can just use the strings from view_file (which are already the "wrong" characters)
    # and replace them with the correct characters.
    # Python text mode will handle the UTF-8 reading.
    # Use replace().
}

# String Replacements
text_replacements = [
    ("â„¢", "™"),
    ("âš¡", "⚡"),
    ("â˜…", "★"),
    ("ðŸ¦…", "🦅"),
    ("ðŸ ‹", "🐋"),
    ("ðŸ•·ï¸", "🕷️"),
    ("ðŸ§ ", "🧠"),
    ("ðŸ›¡ï¸", "🛡️"),
    ("ðŸ•µï¸", "🕵️"),
    ("ðŸ’ ", "💠"),
    ("ðŸ“Š", "📊"),
    ("â†’", "→"),
    ("ðŸ“¡", "📡"),
    ("ðŸ—³ï¸", "🗳️"),
    ("â€”", "—"),
    # Add variations just in case
    ("ðŸ ‹", "🐋"), # The one I saw in view_file
]

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        text_content = f.read()

    new_content = text_content
    for bad, good in text_replacements:
        new_content = new_content.replace(bad, good)

    # Special handling for Orca if it failed simple replace
    # Context: "Orca Mean Reversion"
    # Find the span before it.
    if "🐋" not in new_content and "Orca Mean Reversion" in new_content:
        print("Orca simple replace failed, trying context match...")
        lines = new_content.splitlines()
        for i, line in enumerate(lines):
            if "Orca Mean Reversion" in line:
                # Look 4 lines up for the span with font-size 40px
                for j in range(1, 6):
                    if i - j >= 0:
                        prev_line = lines[i - j]
                        if '<span style="font-size: 40px;">' in prev_line:
                            print(f"Found Orca span at line {i-j+1}: {prev_line}")
                            # Replace the content inside the span
                            start = prev_line.find('>') + 1
                            end = prev_line.rfind('<')
                            if start > 0 and end > start:
                                lines[i - j] = prev_line[:start] + "🐋" + prev_line[end:]
                                print("Fixed Orca line.")
                            break
        new_content = "\n".join(lines)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Successfully processed file.")

except Exception as e:
    print(f"Error: {e}")
