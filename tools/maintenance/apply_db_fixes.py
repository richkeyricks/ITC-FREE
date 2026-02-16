import requests

token = 'sbp_9bb440ecb4fdb362adb4e2bca871fa3190daadea'
project_id = 'nvfpjjmzxkvqbiridpww'
url = f'https://api.supabase.com/v1/projects/{project_id}/database/query'
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("=== APPLY DATABASE FIXES ===\n")

# 1. Create user_configs table
print("--- Creating user_configs table ---")
sql1 = """
CREATE TABLE IF NOT EXISTS user_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_id, key)
);
"""
res1 = requests.post(url, headers=headers, json={'query': sql1})
print(f"Status: {res1.status_code}")
if res1.status_code not in [200, 201]:
    print(f"Error: {res1.text}")
else:
    print("SUCCESS: user_configs table created!")

# 2. Enable RLS on user_configs
print("\n--- Enabling RLS on user_configs ---")
sql2 = """
ALTER TABLE user_configs ENABLE ROW LEVEL SECURITY;

CREATE POLICY IF NOT EXISTS "Users can manage own configs"
ON user_configs
FOR ALL
USING (auth.uid()::text = user_id)
WITH CHECK (auth.uid()::text = user_id);
"""
res2 = requests.post(url, headers=headers, json={'query': sql2})
print(f"Status: {res2.status_code}")

# 3. Add 'name' column to donations table if not exists
print("\n--- Adding 'name' column to donations table ---")
sql3 = """
ALTER TABLE donations ADD COLUMN IF NOT EXISTS name TEXT DEFAULT 'Anonymous';
"""
res3 = requests.post(url, headers=headers, json={'query': sql3})
print(f"Status: {res3.status_code}")
if res3.status_code in [200, 201]:
    print("SUCCESS: 'name' column added to donations!")
else:
    print(f"Error: {res3.text}")

# 4. Verify
print("\n--- Verification ---")
sql4 = "SELECT table_name FROM information_schema.tables WHERE table_name = 'user_configs';"
res4 = requests.post(url, headers=headers, json={'query': sql4})
if res4.status_code in [200, 201] and res4.json():
    print("user_configs: EXISTS ✓")

sql5 = "SELECT column_name FROM information_schema.columns WHERE table_name = 'donations' AND column_name = 'name';"
res5 = requests.post(url, headers=headers, json={'query': sql5})
if res5.status_code in [200, 201] and res5.json():
    print("donations.name: EXISTS ✓")
