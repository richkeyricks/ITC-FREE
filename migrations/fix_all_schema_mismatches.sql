-- MASTER MIGRATION: Fix ALL Schema Mismatches
-- Date: 2026-02-16
-- Purpose: Add ALL missing columns that code tries to sync but don't exist in user_profiles

-- ====================================
-- CRITICAL MISSING COLUMNS
-- ====================================

-- 1. TRADING METRICS (From index.py:145-173)
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS total_volume NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS avg_win NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS avg_loss NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS drawdown_pct NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS win_rate NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS total_deals INTEGER DEFAULT 0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS deals_volume NUMERIC DEFAULT 0.0;

-- 2. MARGIN & ACCOUNT INFO
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS margin_level NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS margin_free NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS margin NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS leverage INTEGER DEFAULT 0;

-- 3. LAST TRADE INFO (Junk keys but code still sends them)
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS last_trade_pair TEXT DEFAULT 'N/A';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS last_trade_type TEXT DEFAULT 'N/A';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS last_trade_lot NUMERIC DEFAULT 0.0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS last_trade_profit NUMERIC DEFAULT 0.0;

-- 4. SIGNAL & MT5 STATUS
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS signal_source TEXT DEFAULT 'Offline';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS mt5_state TEXT DEFAULT 'Offline';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS tg_state TEXT DEFAULT 'Offline';

-- 5. NETWORK & PERFORMANCE
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS mt5_latency INTEGER DEFAULT 0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS ping_ms INTEGER DEFAULT 0;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS internet_ok BOOLEAN DEFAULT true;

-- 6. PRIVACY & UI SETTINGS (Already defined in code)
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS publish_profit BOOLEAN DEFAULT false;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS publish_knowledge BOOLEAN DEFAULT false;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS publish_initials_only BOOLEAN DEFAULT true;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS ui_hints_enabled BOOLEAN DEFAULT true;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS agreement_accepted BOOLEAN DEFAULT false;

-- 7. METADATA
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS app_version TEXT DEFAULT '2.1.2';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS last_seen TIMESTAMPTZ DEFAULT NOW();

-- ====================================
-- INDEXES FOR PERFORMANCE
-- ====================================
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_last_seen ON user_profiles(last_seen);
CREATE INDEX IF NOT EXISTS idx_user_profiles_total_volume ON user_profiles(total_volume);

-- ====================================
-- COMMENTS FOR DOCUMENTATION
-- ====================================
COMMENT ON COLUMN user_profiles.total_volume IS 'Total trading volume across all deals';
COMMENT ON COLUMN user_profiles.avg_win IS 'Average winning trade amount';
COMMENT ON COLUMN user_profiles.avg_loss IS 'Average losing trade amount'; 
COMMENT ON COLUMN user_profiles.win_rate IS 'Win rate percentage (0-100)';
COMMENT ON COLUMN user_profiles.mt5_state IS 'MT5 connection state: Active, Standby, Offline';
COMMENT ON COLUMN user_profiles.tg_state IS 'Telegram bot state: Active, Standby, Offline';

-- ====================================
-- UPDATE EXISTING ROWS
-- ====================================
UPDATE user_profiles SET 
    total_volume = 0.0,
    avg_win = 0.0,
    avg_loss = 0.0,
    win_rate = 0.0,
    total_deals = 0
WHERE total_volume IS NULL;
