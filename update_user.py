import requests
import json

url = ""
params = {"hwid": "eq.db81c319-a3d9-477b-82e5-dbbeb42c79b5"}
headers = {
    "apikey": "",
    "Authorization": "Bearer "
}

try:
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        user = data[0]
        print(f"VERIFIED CLOUD STATUS FOR: {user.get('email')}")
        print(f"Tier: {user.get('subscription_tier')}")
        print(f"Is Pro: {user.get('is_pro')}")
        print(f"Is VIP: {user.get('is_vip')}")
        print(f"Expiry: {user.get('premium_until')}")
    else:
        print("User not found in cloud.")
except Exception as e:
    print(f"Verification Error: {e}")
