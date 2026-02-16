-- Migration: Add country column to user_profiles table
-- Date: 2026-02-16
-- Purpose: Fix schema mismatch error and enable country tracking

-- Add country column with default value
ALTER TABLE user_profiles 
ADD COLUMN IF NOT EXISTS country TEXT DEFAULT 'ID';

-- Add comment for documentation
COMMENT ON COLUMN user_profiles.country IS 'User country code (ISO 3166-1 alpha-2), e.g., ID, US, SG';

-- Create index for faster filtering by country
CREATE INDEX IF NOT EXISTS idx_user_profiles_country ON user_profiles(country);

-- Update existing NULL countries to default
UPDATE user_profiles 
SET country = 'ID' 
WHERE country IS NULL;
