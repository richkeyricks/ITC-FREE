-- Add Telemetry Column for Deep Inspector
alter table public.user_profiles 
add column if not exists telemetry_data jsonb default '{}'::jsonb;

-- Optional: Create a view or index if we plan to query deep into this JSON often
-- For now, just storage is sufficient for the Inspector Panel.

-- Security: Ensure it's viewable by the user (and Admins obviously)
-- Existing RLS policies on user_profiles likely cover this (Select Own).
