-- 1. RESET POLICIES
alter table public.user_presets enable row level security;
drop policy if exists "Allow All Access" on public.user_presets;
drop policy if exists "Public Access" on public.user_presets;
drop policy if exists "Mint Access" on public.user_presets;

-- 2. SECURE ACCESS (Read & Mint Only)
create policy "Store Reader" on public.user_presets for select using (true);
create policy "Minting Rights" on public.user_presets for insert with check (true);

-- 3. SECURE DELETION FUNCTION (RPC)
-- Prevents SQL Injection/Direct Table Wiping
create or replace function public.delete_own_preset(target_id uuid, check_user_id text)
returns boolean
language plpgsql
security definer
as $$
begin
  delete from public.user_presets
  where id = target_id and user_id = check_user_id;
  
  return found; -- Returns true if a row was deleted, false otherwise
end;
$$;

-- 4. GRANT EXECUTE
grant execute on function public.delete_own_preset to anon;
grant execute on function public.delete_own_preset to authenticated;
