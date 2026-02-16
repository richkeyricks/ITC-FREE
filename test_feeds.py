import requests
import xml.etree.ElementTree as ET

def test_feeds():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://www.forexfactory.com/'
    }
    
    urls = [
        "https://nfs.faireconomy.media/ff_calendar_thisweek.xml",
        "https://www.myfxbook.com/rss/forex-economic-calendar"
    ]
    
    for url in urls:
        print(f"Testing: {url}")
        try:
            res = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {res.status_code}")
            if res.status_code == 200:
                print(f"Content Length: {len(res.text)}")
                print(f"Snippet: {res.text[:200]}")
            else:
                print(f"Response Headers: {res.headers}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_feeds()
