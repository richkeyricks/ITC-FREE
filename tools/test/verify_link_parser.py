import re

def test_link_parser(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    parts = re.split(pattern, text)
    
    print(f"Input: {text}")
    print(f"Parts: {parts}")
    
    for i in range(0, len(parts), 3):
        print(f"Text Segment {i//3}: '{parts[i]}'")
        if i + 1 < len(parts):
            print(f"Link {i//3}: Label='{parts[i+1]}', URL='{parts[i+2]}'")
    print("-" * 20)

# Test cases
test_cases = [
    "Buka [my.telegram.org](https://my.telegram.org) sekarang.",
    "Langkah: 1. [Link1](url1) 2. [Link2](url2) selesai.",
    "Teks tanpa link.",
    "[Full Link](https://test.com)"
]

for tc in test_cases:
    test_link_parser(tc)
