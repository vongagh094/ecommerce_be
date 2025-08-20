-- thêm cột auction_id cho calendar_availability
ALTER TABLE calendar_availability
ADD COLUMN IF NOT EXISTS auction_id UUID;

--xóa unique constraint cũ (đang chặn trường hợp có auction_id khác nhau)
ALTER TABLE calendar_availability
DROP CONSTRAINT IF EXISTS calendar_availability_property_id_date_key;

-- đảm bảo 2 partial unique indexes tồn tại (idempotent)
CREATE UNIQUE INDEX IF NOT EXISTS calendar_availability_with_auction_unique_idx
  ON calendar_availability (property_id, auction_id, date)
  WHERE auction_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS calendar_availability_legacy_unique_idx
  ON calendar_availability (property_id, date)
  WHERE auction_id IS NULL;
BEGIN;

--update index
-- Drop constraint cũ
ALTER TABLE bids DROP CONSTRAINT IF EXISTS chk_bid_dates;

-- Tạo constraint mới cho phép same day
ALTER TABLE bids ADD CONSTRAINT chk_bid_dates
CHECK (check_out >= check_in);

COMMIT;

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS after_insert_auction_trigger ON auctions;

-- Create or replace the trigger function
CREATE OR REPLACE FUNCTION after_insert_auction()
RETURNS TRIGGER AS $$
DECLARE
    loop_date DATE;
BEGIN
    -- Loop through each day in the auction period
    loop_date := NEW.start_date;

    WHILE loop_date <= NEW.end_date LOOP
        -- Use INSERT ... ON CONFLICT to handle duplicates on (property_id, date, auction_id)
        INSERT INTO calendar_availability (
            property_id,
            date,
            auction_id,
            price_amount,
            is_available,
            created_at,
            updated_at
        ) VALUES (
            NEW.property_id,
            loop_date,
            NEW.id::TEXT,
            0,
            TRUE,
            now(),
            now()
        ) ON CONFLICT (property_id, date, auction_id)
        DO UPDATE SET
            price_amount = EXCLUDED.price_amount,
            is_available = EXCLUDED.is_available,
            updated_at = now();

        loop_date := loop_date + INTERVAL '1 day';
    END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER after_insert_auction_trigger
    AFTER INSERT ON auctions
    FOR EACH ROW
    EXECUTE FUNCTION after_insert_auction();