import requests
import json

url = "https://api.supabase.com/v1/projects/nvfpjjmzxkvqbiridpww/database/query"
headers = {
    "Authorization": "Bearer sbp_9bb440ecb4fdb362adb4e2bca871fa3190daadea",
    "Content-Type": "application/json"
}

sql = """
CREATE TABLE IF NOT EXISTS public.entitlements (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    tier TEXT CHECK (tier IN ('standard', 'gold', 'platinum', 'institutional')),
    is_lifetime BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.entitlements ENABLE ROW LEVEL SECURITY;

DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read access to entitlements'
    ) THEN
        CREATE POLICY "Allow public read access to entitlements" ON public.entitlements FOR SELECT TO anon, authenticated USING (true);
    END IF;
END $$;
"""

try:
    response = requests.post(url, headers=headers, json={"query": sql})
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201]:
        print("SUCCESS: Database table and policy created.")
    else:
        print(f"ERROR: {response.text}")
except Exception as e:
    print(f"EXCEPTION: {str(e)}")
