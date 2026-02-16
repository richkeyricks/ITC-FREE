-- Database Migration V3: God Mode Telemetry Restoration
-- Run this in the Supabase SQL Editor to enable full 63-parameter sync.

ALTER TABLE user_profiles
ADD COLUMN IF NOT EXISTS timezone text,
ADD COLUMN IF NOT EXISTS boot_time text,
ADD COLUMN IF NOT EXISTS cpu_load text,
ADD COLUMN IF NOT EXISTS gpu_model text,
ADD COLUMN IF NOT EXISTS mt5_latency integer DEFAULT 0,
ADD COLUMN IF NOT EXISTS last_trade_magic text,
ADD COLUMN IF NOT EXISTS sltp_mode text,
ADD COLUMN IF NOT EXISTS trade_hours text,
ADD COLUMN IF NOT EXISTS deals_total integer DEFAULT 0,
ADD COLUMN IF NOT EXISTS deals_volume double precision DEFAULT 0,
ADD COLUMN IF NOT EXISTS avg_win double precision DEFAULT 0,
ADD COLUMN IF NOT EXISTS avg_loss double precision DEFAULT 0,
ADD COLUMN IF NOT EXISTS drawdown_pct double precision DEFAULT 0,
ADD COLUMN IF NOT EXISTS margin double precision DEFAULT 0,
ADD COLUMN IF NOT EXISTS margin_free double precision DEFAULT 0,
ADD COLUMN IF NOT EXISTS margin_level double precision DEFAULT 0;

COMMENT ON TABLE user_profiles IS 'Enterprise User Profiles with 63-parameter God Mode Telemetry';
