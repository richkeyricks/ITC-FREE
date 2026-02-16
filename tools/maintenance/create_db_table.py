import requests
import json

url = "https://nvfpjjmzxkvqbiridpww.supabase.co/rest/v1/"
# Menggunakan Secret Key (Service Role) untuk menjalankan DDL
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im52ZnBqam16eGt2cWJpcmlkcHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwOTQ0MjIsImV4cCI6MjA4NDY3MDQyMn0.OWbiv4Xq8TIRE86ScWbX3HJ2013dWPLIsJ1L09j88Fs",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im52ZnBqam16eGt2cWJpcmlkcHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwOTQ0MjIsImV4cCI6MjA4NDY3MDQyMn0.OWbiv4Xq8TIRE86ScWbX3HJ2013dWPLIsJ1L09j88Fs",
    "Content-Type": "application/json"
}

# SQL DDL
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

# Supabase REST API doesn't support direct SQL execution easily without a function wrapper.
# However, I can try the execute_sql tool from MCP now that I have the details.
print("Executing SQL via script is tricky for DDL. I will attempt direct DB migration steps.")
