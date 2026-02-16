import requests

token = 'sbp_9bb440ecb4fdb362adb4e2bca871fa3190daadea'
project_id = 'nvfpjjmzxkvqbiridpww'
url = f'https://api.supabase.com/v1/projects/{project_id}/database/query'
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("=== CEK SKEMA DONATIONS & USER_CONFIGS ===\n")

# 1. Donations columns
print("--- KOLOM donations ---")
sql1 = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'donations' ORDER BY ordinal_position;"
res1 = requests.post(url, headers=headers, json={'query': sql1})
if res1.status_code in [200, 201]:
    for col in res1.json():
        print(f"  {col['column_name']}: {col['data_type']}")

# 2. user_configs columns
print("\n--- KOLOM user_configs ---")
sql2 = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'user_configs' ORDER BY ordinal_position;"
res2 = requests.post(url, headers=headers, json={'query': sql2})
if res2.status_code in [200, 201]:
    data = res2.json()
    if data:
        for col in data:
            print(f"  {col['column_name']}: {col['data_type']}")
    else:
        print("  [TABLE DOES NOT EXIST!]")

# 3. Check if user_configs table exists
print("\n--- CEK TABLE user_configs EXISTS ---")
sql3 = "SELECT table_name FROM information_schema.tables WHERE table_name = 'user_configs';"
res3 = requests.post(url, headers=headers, json={'query': sql3})
if res3.status_code in [200, 201]:
    data = res3.json()
    if data:
        print("  EXISTS: True")
    else:
        print("  EXISTS: False - PERLU BUAT TABEL!")
