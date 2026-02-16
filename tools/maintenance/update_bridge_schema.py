import requests

url = "https://api.supabase.com/v1/projects/nvfpjjmzxkvqbiridpww/database/query"
headers = {
    "Authorization": "Bearer sbp_9bb440ecb4fdb362adb4e2bca871fa3190daadea",
    "Content-Type": "application/json"
}

sql = """
-- SYSTEM COMMANDS TABLE (For Remote Control)
CREATE TABLE IF NOT EXISTS public.system_commands (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    action TEXT NOT NULL,
    params JSONB DEFAULT '{}'::jsonb,
    status TEXT DEFAULT 'PENDING',
    origin TEXT DEFAULT 'WEB_PORTAL',
    created_at TIMESTAMPTZ DEFAULT now(),
    processed_at TIMESTAMPTZ
);

-- SYSTEM LOGS TABLE (For Neural Stream)
CREATE TABLE IF NOT EXISTS public.system_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    event TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ENABLE RLS
ALTER TABLE public.system_commands ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_logs ENABLE ROW LEVEL SECURITY;

-- POLICIES
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public access to commands') THEN
        CREATE POLICY "Allow public access to commands" ON public.system_commands FOR ALL TO anon, authenticated USING (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public access to logs') THEN
        CREATE POLICY "Allow public access to logs" ON public.system_logs FOR ALL TO anon, authenticated USING (true);
    END IF;
END $$;
"""

try:
    response = requests.post(url, headers=headers, json={"query": sql})
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201]:
        print("SUCCESS: Command Bridge schema updated in Supabase.")
    else:
        print(f"ERROR: {response.text}")
except Exception as e:
    print(f"EXCEPTION: {str(e)}")
