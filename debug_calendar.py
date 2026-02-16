import requests
try:
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    print(f"Fetching {url}...")
    res = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {res.status_code}")
    print("Content Preview (First 1000 chars):")
    print(res.text[:1000])
    
    import xml.etree.ElementTree as ET
    from datetime import datetime
    root = ET.fromstring(res.text)
    events = root.findall('event')
    print(f"\nTotal Events found in XML: {len(events)}")
    
    # Print dates of last few events to see if it covers the weekend
    if events:
        print("Last 5 events:")
        for e in events[-5:]:
            date = e.find('date').text
            time = e.find('time').text
            currency = e.find('country').text
            print(f"- {date} {time} {currency}")

except Exception as e:
    print(f"Error: {e}")
