-- Database Seeding: Verified Signal Marketplace (Full 10-Channel Set)
-- Run this in the Supabase SQL Editor to populate the Signal Hub.

DELETE FROM verified_channels; -- Clear previous to avoid duplicates

INSERT INTO verified_channels (name, link, accuracy_pct, subscribers, description_id, description_en, language, is_featured)
VALUES 
-- OFFICIAL & FEATURED
('ITC Enterprise Verified', 'https://t.me/richkeyrick', 98, '15k', 'Channel Resmi ITC dengan audit sinyal AI tingkat lanjut.', 'Official ITC Channel with advanced AI signal auditing.', 'ALL', true),

-- GLOBAL PREMIUM (EN)
('SureShotFX', 'https://t.me/sureshotfx', 85, '53k+', 'Sinyal Forex & Gold dengan akurasi tinggi (80-90%) didukung analisa teknikal mendalam.', 'High accuracy Forex & Gold signals (80-90%) with deep technical analysis.', 'EN', true),
('Learn2Trade', 'https://t.me/learn2tradesignals', 82, '17k+', 'Provider sinyal legendaris dengan edukasi trading lengkap dan 3 level Take Profit.', 'Legendary signal provider with complete education and 3-level Take Profit.', 'EN', false),
('Vasily Trader', 'https://t.me/vasilytrader', 75, '26k+', 'Fokus pada Price Action murni dan transparansi performa trading tanpa janji manis.', 'Focused on pure Price Action and performance transparency without sweet promises.', 'EN', false),
('FX Scalping Elite', 'https://t.me/richkeyrick', 92, '145k', 'Sinyal forex super cepat untuk scalping harian.', 'Ultra-fast forex signals for daily scalping.', 'EN', false),
('XAUUSD PRO Signals', 'https://t.me/richkeyrick', 89, '82k', 'Ahli sinyal Emas dengan akurasi tinggi & manajemen risiko ketat.', 'Gold signal expert with high accuracy & tight risk management.', 'EN', false),

-- INDONESIA LOCAL (ID)
('Apex Trading ID', 'https://t.me/apextradingid', 80, '10k+', 'Komunitas trader Indonesia aktif dengan update market harian dan sinyal akurat jam Asia.', 'Active Indonesian trading community with daily market updates and accurate Asian session signals.', 'ID', true),
('Kalsum FX (Gold)', 'https://t.me/kalsumfx', 78, '15k+', 'Spesialis sinyal Gold (XAUUSD) Indonesia dengan manajemen risiko yang sangat disiplin.', 'Indonesian Gold (XAUUSD) specialist with highly disciplined risk management.', 'ID', false),
('IndoTradX Ultra', 'https://t.me/richkeyrick', 72, '12k', 'Analisa teknikal harian dan sinyal high-probability untuk pasar lokal.', 'Daily technical analysis and high-probability signals for local markets.', 'ID', false),
('Nusantara Crypto', 'https://t.me/richkeyrick', 65, '8k', 'Fokus pada aset crypto blue-chip (BTC/ETH) dengan update fundamental harian.', 'Focus on blue-chip crypto assets (BTC/ETH) with daily fundamental updates.', 'ID', false);

-- Note: The 'Under Audit' label will be triggered in UI for channels with accuracy < 75% or specific status.
