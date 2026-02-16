import requests
import json

print("=== TEST VERCEL PAYMENT API ===\n")

VERCEL_API = "https://www.telegramcopytrading.com/api/pay"

payload = {
    "order_id": "TEST-ORDER-123",
    "amount": 100000,
    "currency": "IDR",
    "preset_name": "Test Product (IDR)",
    "customer_email": "test@example.com"
}

print(f"Endpoint: {VERCEL_API}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\nSending POST request...")

try:
    response = requests.post(VERCEL_API, json=payload, timeout=15)
    print(f"\nStatus Code: {response.status_code}")
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ SUCCESS!")
        print(f"Token: {data.get('token', 'N/A')}")
        print(f"Redirect URL: {data.get('redirect_url', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Exception: {e}")
