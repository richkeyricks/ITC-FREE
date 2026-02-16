import requests
import json

token = 'sbp_9bb440ecb4fdb362adb4e2bca871fa3190daadea'
project_id = 'nvfpjjmzxkvqbiridpww'
url = f'https://api.supabase.com/v1/projects/{project_id}/database/query'
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

print("=== CREATING ROADMAP TABLES ===\n")

# 1. Create roadmap_items table
print("--- Creating roadmap_items table ---")
sql1 = """
CREATE TABLE IF NOT EXISTS roadmap_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT DEFAULT 'FEATURE',
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'PROPOSED',
    votes INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    created_by TEXT
);
"""
res1 = requests.post(url, headers=headers, json={'query': sql1})
print(f"Status: {res1.status_code}")

# 2. Create roadmap_votes table (track who voted)
print("\n--- Creating roadmap_votes table ---")
sql2 = """
CREATE TABLE IF NOT EXISTS roadmap_votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id UUID REFERENCES roadmap_items(id),
    user_id TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(item_id, user_id)
);
"""
res2 = requests.post(url, headers=headers, json={'query': sql2})
print(f"Status: {res2.status_code}")

# 3. Insert default roadmap items
print("\n--- Inserting default roadmap items ---")
sql3 = """
INSERT INTO roadmap_items (category, title, description, status, votes) VALUES
('MOBILE APP', 'ITC Mobile App (iOS/Android)', 'Native mobile application for real-time signal notifications and one-tap copy trading.', 'IN PROGRESS', 35),
('AI ENGINE', 'Neural Engine V2 (Hedge Fund Grade)', 'Integration with institutional data feeds and sentiment analysis for higher accuracy.', 'PLANNED', 88),
('NETWORK', 'Decentralized Signal Network', 'Blockchain-based signal verification to ensure 100% transparency and immutability.', 'PROPOSED', 12),
('ECOSYSTEM', 'Multi-Broker Support', 'Seamless integration with all major brokers worldwide including cTrader and TradingView.', 'PROPOSED', 45),
('AUTOMATION', 'Smart Risk Manager', 'AI-powered position sizing and automated stop-loss adjustment based on market volatility.', 'WHITELISTED', 97)
ON CONFLICT DO NOTHING;
"""
res3 = requests.post(url, headers=headers, json={'query': sql3})
print(f"Status: {res3.status_code}")

# 4. Verify
print("\n--- Verification ---")
sql4 = "SELECT COUNT(*) as count FROM roadmap_items;"
res4 = requests.post(url, headers=headers, json={'query': sql4})
if res4.status_code in [200, 201]:
    data = res4.json()
    if data:
        print(f"roadmap_items count: {data[0]['count']}")
