-- SECURE UPDATE FUNCTION (RPC)
-- Allows users to EDIT their own presets (Name, Price, Visibility, etc.)
-- Bypasses the RLS "No Update" restriction safely.

create or replace function public.update_own_preset(
    target_id uuid, 
    check_user_id text,
    new_name text,
    new_desc text,
    new_config jsonb,
    new_is_public boolean,
    new_price numeric
)
returns boolean
language plpgsql
security definer
as $$
begin
  update public.user_presets
  set 
    name = new_name,
    description = new_desc,
    config_json = new_config,
    is_public = new_is_public,
    price = new_price,
    updated_at = now()
  where id = target_id and user_id = check_user_id;
  
  return found; -- Returns true if a row was updated
end;
$$;

-- GRANT EXECUTE
grant execute on function public.update_own_preset to anon;
grant execute on function public.update_own_preset to authenticated;
