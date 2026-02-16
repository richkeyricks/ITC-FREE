import requests
import json

url = "https://api.supabase.com/v1/projects/nvfpjjmzxkvqbiridpww/config/auth"
headers = {
    "Authorization": "Bearer sbp_9bb440ecb4fdb362adb4e2bca871fa3190daadea"
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        config = response.json()
        print("Keys in Auth Config:")
        print(list(config.keys()))
        # Print SMTP related keys specifically
        smtp_keys = [k for k in config.keys() if 'smtp' in k.lower() or 'mail' in k.lower()]
        print("\nSMTP Related Keys:")
        for k in smtp_keys:
            print(f"{k}: {config[k]}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Exception: {str(e)}")
