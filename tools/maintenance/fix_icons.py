
import os
import re

file_path = r"c:\APLIKASI YANG DIBUAT\TELEGRAM MT5\web\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix broken URL (remove newline)
# The broken string is likely "https://ra\nndomuser.me" or "https://ra\r\nndomuser.me"
fixed_content = re.sub(r'https://ra[\r\n]+ndomuser\.me', 'https://randomuser.me', content)

if fixed_content != content:
    print("Fixed broken URL.")
else:
    print("Warning: Broken URL not found or regex mismatch.")
    # Fallback: look for the split string manually
    if "https://ra" in content and "ndomuser.me" in content:
        print("Found parts of URL, trying simpler replace.")
        fixed_content = content.replace("https://ra\nndomuser.me", "https://randomuser.me")

# 2. Replace DAO Governance Emoji with SVG
# Target:
# <div
#     style="background: #1a1a1a; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff;">
#     🗳️ </div>

# We will look for "DAO Governance" and backtrack to find the emoji div.
lines = fixed_content.splitlines()
for i, line in enumerate(lines):
    if "DAO Governance" in line:
        # Search backwards for the emoji div
        for j in range(1, 10):
            if i - j >= 0:
                prev_line = lines[i - j]
                if "🗳️" in prev_line or "\U0001f5f3" in prev_line:
                    print(f"Found emoji at line {i-j+1}")
                    # Replace the content of this line (and potentially previous lines if it's multi-line div)
                    # Actually, the div style is inline.
                    # I'll just replace the inner content of the div?
                    # or the whole div. 
                    # The div starts a few lines back.
                    
                    # Simpler approach: regex replace the emoji if found.
                    pass

# Let's use regex for the emoji part too, it's safer than line iterating if format varies.
# Match the div content containing the emoji.
# The emoji might be on its own line.
pattern = r'(<div[^>]*>)\s*🗳️\s*(</div>)'
replacement = r'\1<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"></polyline><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>\2'

# We also want to update the STYLE of that div to match the "Whale Alert" one (transparent bg, thin border).
# The old style: background: #1a1a1a; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff;
# The new style: background: rgba(255,255,255,0.05); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--accent); border: 1px solid rgba(255,255,255,0.1);

# So we should find the WHOLE block.
block_pattern = r'(<div\s+style="background: #1a1a1a; width: 40px; height: 40px;[^"]*">\s*🗳️\s*</div>)'
svg_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"></polyline><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>'
new_style = 'background: rgba(255,255,255,0.05); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--accent); border: 1px solid rgba(255,255,255,0.1);'
new_block = f'<div style="{new_style}">\n                                {svg_icon}</div>'

fixed_content_2 = re.sub(block_pattern, new_block, fixed_content, flags=re.DOTALL)

if fixed_content_2 != fixed_content:
    print("Fixed DAO Governance icon.")
else:
    print("Warning: DAO Governance icon block not found.")
    # Fallback: simple text replace of the emoji line if block match failed
    if "🗳️" in fixed_content:
        print("Falling back to simple emoji replace.")
        fixed_content_2 = fixed_content.replace("🗳️", svg_icon)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content_2)
