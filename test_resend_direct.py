import os
import requests
import json

# API KEY DARI .ENV ANDA
RESEND_API_KEY = "re_JYuGVYXj_5fBA3UCDEBJowjYLGP5WSiWm"

def test_resend():
    print("Testing Resend API...")
    
    url = "https://api.resend.com/emails"
    
    payload = {
        "from": "ITC Support <noreply@telegramcopytrading.com>",
        "to": ["richkeyrick@gmail.com"],
        "subject": "TEST EMAIL DARI SCRIPT",
        "html": "<strong>It works!</strong> API Key ini valid."
    }
    
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ SUKSES! API Key Valid & Domain Verified.")
            print("Masalah bukan di API Key, tapi di settingan Supabase.")
        else:
            print("\n❌ GAGAL! Ada masalah dengan API Key atau Domain.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_resend()
