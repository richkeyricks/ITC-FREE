"""
ISOLATED DIAGNOSTIC SCRIPT
Tests Supabase connection without touching any application code.
"""
import os
import sys

# Add src to path
_base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_base_dir, 'src'))

from dotenv import load_dotenv
load_dotenv()

print("=" * 50)
print("SUPABASE DIAGNOSTIC")
print("=" * 50)

# Step 1: Check ENV
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
print(f"[1] SUPABASE_URL: {'OK' if url else 'MISSING'}")
print(f"[2] SUPABASE_KEY: {'OK' if key else 'MISSING'}")

if not url or not key:
    print("\n[FATAL] Missing credentials. Cannot proceed.")
    sys.exit(1)

# Step 2: Test Connection
from supabase import create_client
try:
    client = create_client(url, key)
    print(f"[3] Client Created: OK")
except Exception as e:
    print(f"[3] Client Created: FAILED - {e}")
    sys.exit(1)

# Step 3: Test Auth Session
try:
    session = client.auth.get_session()
    if session and session.user:
        print(f"[4] Active Session: YES - {session.user.email}")
    else:
        print(f"[4] Active Session: NO (Normal if not logged in)")
except Exception as e:
    print(f"[4] Session Check: FAILED - {e}")

# Step 4: Test OAuth URL Generation
try:
    res = client.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": "https://telegramcopytrade.vercel.app/auth-callback.html"
        }
    })
    if res and res.url:
        print(f"[5] OAuth URL: OK")
        print(f"    URL Preview: {res.url[:80]}...")
    else:
        print(f"[5] OAuth URL: FAILED - No URL returned")
except Exception as e:
    print(f"[5] OAuth URL: FAILED - {e}")

# Step 5: Test Email Login (dry run - will fail but shows if API works)
print(f"\n[6] Email Login Test (expects failure - just testing API):")
try:
    res = client.auth.sign_in_with_password({"email": "test@test.com", "password": "wrong"})
    print(f"    Result: Unexpected success")
except Exception as e:
    err = str(e)
    if "Invalid login credentials" in err:
        print(f"    Result: API WORKS (got expected 'Invalid credentials' error)")
    else:
        print(f"    Result: {err}")

print("\n" + "=" * 50)
print("DIAGNOSTIC COMPLETE")
print("=" * 50)
