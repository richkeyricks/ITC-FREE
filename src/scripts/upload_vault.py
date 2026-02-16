import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def upload_secrets():
    print("🚀 Starting ITC +AI Cloud Vault Upload...")
    load_dotenv(override=True)
    
    # 1. ADMIN CONNECTION
    url = os.getenv("SUPABASE_URL")
    # CRITICAL: Use Service Role Key for Admin Upsert
    role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not role_key:
        print("❌ ERROR: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY missing from .env")
        return

    try:
        supabase: Client = create_client(url, role_key)
        print("✅ Supabase Admin Connection Established.")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # 2. DEFINE SECRETS MAPPING
    # Format: (env_key, vault_key_name, service_name)
    mapping = [
        ("MASTER_GROQ_KEY", "MASTER_GROQ_KEY", "AI"),
        ("MIDTRANS_SERVER_KEY", "MIDTRANS_SERVER_KEY", "Payment"),
        ("MIDTRANS_CLIENT_KEY", "MIDTRANS_CLIENT_KEY", "Payment"),
        ("MIDTRANS_MERCHANT_ID", "MIDTRANS_MERCHANT_ID", "Payment"),
        ("MIDTRANS_IS_PRODUCTION", "MIDTRANS_IS_PRODUCTION", "Payment"),
        ("RESEND_API_KEY", "RESEND_API_KEY", "Email"),
        ("SERPER_API_KEY", "SERPER_API_KEY", "Analytics"),
        ("CLOUDFLARE_API_KEY", "CLOUDFLARE_API_KEY", "AI"),
        ("CLOUDFLARE_ID", "CLOUDFLARE_ID", "AI"),
        ("OLLAMA_API_KEY", "OLLAMA_API_KEY", "AI")
    ]

    # 3. UPSERT LOOP
    success_count = 0
    fail_count = 0
    
    for env_key, key_name, service in mapping:
        val = os.getenv(env_key)
        if not val:
            print(f"⚠️ Skipping {key_name}: Value not found in .env")
            continue
            
        data = {
            "key_name": key_name,
            "key_value": str(val).strip("'").strip('"'),
            "service": service
        }
        
        try:
            # Upsert by key_name (requires UNIQUE constraint on key_name)
            supabase.table("app_secrets").upsert(data, on_conflict="key_name").execute()
            print(f"✅ Uploaded: {key_name} [{service}]")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed {key_name}: {e}")
            fail_count += 1

    print("\n" + "="*40)
    print(f"🏁 UPLOAD COMPLETE")
    print(f"📊 Success: {success_count} | Failed: {fail_count}")
    print("="*40)
    if success_count > 0:
        print("💡 The application will now use these keys from the cloud on next boot.")

if __name__ == "__main__":
    upload_secrets()
