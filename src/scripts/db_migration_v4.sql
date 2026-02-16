-- Database Migration V4: RLS Security & Performance Fix
-- Run this in the Supabase SQL Editor to resolve "OFFLINE" sync blockages.

-- 1. DROP OLD RESTRICTIVE POLICIES
DROP POLICY IF EXISTS "Admin Update Access" ON user_profiles;
DROP POLICY IF EXISTS "Allow admin read user_profiles" ON user_profiles;

-- 2. CREATE PERMISSIVE OWN-ROW POLICIES
-- Allow users to see their own profile
CREATE POLICY "Users can select own profile" ON user_profiles 
FOR SELECT USING (hwid = auth.uid()::text);

-- Allow users to create their own profile (Required for first-time upsert)
CREATE POLICY "Users can insert own profile" ON user_profiles 
FOR INSERT WITH CHECK (hwid = auth.uid()::text);

-- Allow users to update their own profile (Essential for heartbeats)
CREATE POLICY "Users can update own profile" ON user_profiles 
FOR UPDATE USING (hwid = auth.uid()::text) 
WITH CHECK (hwid = auth.uid()::text);

-- 3. GLOBAL ADMIN OVERRIDE (For Richkeyrick)
-- Admin can see and manage all profiles
CREATE POLICY "Admin full access" ON user_profiles 
FOR ALL USING (auth.jwt() ->> 'email' = 'richkeyrick@gmail.com');

-- 4. PERFORMANCE INDICES
CREATE INDEX IF NOT EXISTS idx_profiles_hwid ON user_profiles(hwid);
CREATE INDEX IF NOT EXISTS idx_profiles_email ON user_profiles(email);

-- 5. ENSURE RLS IS ACTIVE
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

COMMENT ON POLICY "Users can update own profile" ON user_profiles IS 'Enables real-time heartbeats and telemetry updates.';
