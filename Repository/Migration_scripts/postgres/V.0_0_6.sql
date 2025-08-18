BEGIN;

-- Drop constraint cũ
ALTER TABLE bids DROP CONSTRAINT IF EXISTS chk_bid_dates;

-- Tạo constraint mới cho phép same day
ALTER TABLE bids ADD CONSTRAINT chk_bid_dates
CHECK (check_out >= check_in);

COMMIT;