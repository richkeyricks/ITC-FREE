
import requests
import xml.etree.ElementTree as ET
import re

urls = {
    "FF Thisweek": "https://nfs.faireconomy.media/ff_calendar_thisweek.xml",
    "FF Nextweek": "https://nfs.faireconomy.media/ff_calendar_nextweek.xml",
    "Myfxbook": "https://www.myfxbook.com/rss/forex-economic-calendar",
    "DailyFX": "https://www.dailyfx.com/feeds/economic-calendar"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

for name, url in urls.items():
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"--- {name} ---")
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print(f"Length: {len(res.text)}")
            root = ET.fromstring(res.text)
            items = root.findall('.//item') if "rss" in url or "feeds" in url else list(root)
            print(f"Items found: {len(items)}")
            if items:
                # Print sample title/date
                if "faireconomy" in url:
                    print(f"Sample: {items[0].find('title').text} on {items[0].find('date').text}")
                else:
                    print(f"Sample: {items[0].find('title').text}")
        else:
            print(f"Error: {res.text[:100]}")
    except Exception as e:
        print(f"Error {name}: {e}")
    print("\n")
