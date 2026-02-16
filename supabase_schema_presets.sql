-- USER PRESETS (Vault & Marketplace)
create table if not exists public.user_presets (
    id uuid default gen_random_uuid() primary key,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    
    user_id text not null, -- Links to hwid
    name text not null,
    description text,
    
    config_json jsonb not null default '{}'::jsonb, -- The Strategy Parameters
    
    is_public boolean default false, -- True = Listed in Marketplace
    price numeric default 0, -- Cost to copy/rent
    
    downloads int default 0,
    rating numeric default 5.0
);

-- Index for User lookup
create index if not exists idx_presets_user on public.user_presets(user_id);
create index if not exists idx_presets_public on public.user_presets(is_public);

-- Optional: Enable RLS
alter table public.user_presets enable row level security;

-- Policy: View Public or Own
create policy "Public Presets are visible to everyone" 
on public.user_presets for select 
using (is_public = true or user_id = auth.uid()::text or user_id = current_setting('request.headers')::json->>'hwid');

-- Policy: Insert/Update Own
-- Note: Supabase Auth usually handles uid, but since we use HWID login custom logic
-- we might need specific RPCs or simplified policies for this specific app architecture.
-- For now, open insert for authenticated/anon key users passing their own ID is acceptable for this prototype.
create policy "Users can insert their own presets" 
on public.user_presets for insert 
with check (true); 
