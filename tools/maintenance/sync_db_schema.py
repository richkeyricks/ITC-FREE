import requests
import json

url = "https://api.supabase.com/v1/projects/nvfpjjmzxkvqbiridpww/database/query"
headers = {
    "Authorization": "Bearer sbp_9bb440ecb4fdb362adb4e2bca871fa3190daadea",
    "Content-Type": "application/json"
}

sql = """
ALTER TABLE public.entitlements 
ADD COLUMN IF NOT EXISTS source TEXT,
ADD COLUMN IF NOT EXISTS payment_processor_id TEXT,
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
"""

try:
    response = requests.post(url, headers=headers, json={"query": sql})
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201]:
        print("SUCCESS: Table schema synchronized with Edge Function logic.")
    else:
        print(f"ERROR: {response.text}")
except Exception as e:
    print(f"EXCEPTION: {str(e)}")
