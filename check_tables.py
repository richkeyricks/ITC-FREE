import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
    exit(1)

try:
    client = create_client(url, key)
    # There is no direct "list tables" in the python client easily without admin privs or introspection.
    # But we can try to query `information_schema.tables` if we have permissions, 
    # OR we can just test the tables we expect to see.
    
    # Attempt 1: Introspection (often blocked for anon keys, but let's try)
    # We can try to select from a few known tables to see if they exist.
    
    known_tables = [
        "user_profiles",
        "user_presets", 
        "marketplace_orders",
        "trades",
        "logs",
        "activity_logs",
        "messages",
        "quiz_scores",
        "leaderboard_profit",
        "leaderboard_accuracy", 
        "leaderboard_consistency",
        "leaderboard_knowledge",
        "admin_broadcasts",
        "ai_usage_daily" # from client code
    ]
    
    print(f"Checking access to {len(known_tables)} expected tables...")
    
    for table in known_tables:
        try:
            # Just try to fetch 1 row to check existence/access
            res = client.table(table).select("*", count="exact").limit(1).execute()
            print(f"[OK] {table} (Count: {res.count if hasattr(res, 'count') else '?'})")
        except Exception as e:
            print(f"[ERR] {table}: {e}")

except Exception as e:
    print(f"Client Init Error: {e}")
