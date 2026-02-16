import requests
import json
import os

RESEND_API_KEY = "re_JYuGVYXj_5fBA3UCDEBJowjYLGP5WSiWm"

def force_verify():
    print("⏳ MENCARI DOMAIN ID...")
    
    # 1. LIST DOMAINS
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.get("https://api.resend.com/domains", headers=headers)
        if res.status_code != 200:
            print(f"❌ Error Listing Domains: {res.text}")
            return

        domains = res.json().get("data", [])
        target_id = None
        
        for d in domains:
            print(f"- Found: {d['name']} (Status: {d['status']})")
            if d['name'] == "telegramcopytrading.com":
                target_id = d['id']
                
        if not target_id:
            print("❌ Domain telegramcopytrading.com tidak ditemukan di akun Resend ini!")
            return
            
        print(f"✅ Domain ID Ditemukan: {target_id}")
        print("🚀 MENCOBA PAKSA VERIFIKASI (FORCE VERIFY)...")
        
        # 2. FORCE VERIFY
        verify_url = f"https://api.resend.com/domains/{target_id}/verify"
        verify_res = requests.post(verify_url, headers=headers)
        
        if verify_res.status_code == 200:
            print("\n✅ REQUEST SUKSES! Resend sedang mengecek ulang sekarang.")
            print("Tunggu 1-2 menit, lalu cek dashboard lagi.")
        else:
            print(f"\n⚠️ GAGAL MEMAKSA VERIFIKASI: {verify_res.text}")
            print("Kemungkinan karena server DNS memang belum propagasi (masih kosong).")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_verify()
