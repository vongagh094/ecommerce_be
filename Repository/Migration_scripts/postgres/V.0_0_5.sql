-- GIẢI PHÁP: Hỗ trợ cả dữ liệu cũ (auction_id = NULL) và mới (auction_id có giá trị)

BEGIN;
--
-- ALTER TABLE calendar_availability
-- DROP CONSTRAINT calendar_availability_property_id_date_key;

-- Bước 1: Thêm auction_id column nếu chưa có
ALTER TABLE calendar_availability 
ADD COLUMN IF NOT EXISTS auction_id UUID;

-- Bước 2: Tạo 2 partial unique indexes riêng biệt
-- Index cho data MỚI (có auction_id)
DROP INDEX IF EXISTS calendar_availability_with_auction_unique_idx;
CREATE UNIQUE INDEX calendar_availability_with_auction_unique_idx 
ON calendar_availability (property_id, auction_id, date) 
WHERE auction_id IS NOT NULL;

-- Index cho data CŨ (auction_id = NULL)  
DROP INDEX IF EXISTS calendar_availability_legacy_unique_idx;
CREATE UNIQUE INDEX calendar_availability_legacy_unique_idx 
ON calendar_availability (property_id, date) 
WHERE auction_id IS NULL;

-- Bước 3: Function xử lý cả 2 trường hợp
DROP FUNCTION IF EXISTS insert_calendar_availability_from_bid;

CREATE OR REPLACE FUNCTION insert_calendar_availability_from_bid(
    p_bid_id UUID,
    p_property_id BIGINT,
    p_auction_id UUID,  -- Có thể NULL
    p_check_in DATE,
    p_check_out DATE,
    p_price_amount NUMERIC,
    p_is_available BOOLEAN
)
RETURNS VOID AS $$
DECLARE
    loop_date DATE;
    price_per_day NUMERIC;
    total_days INTEGER;
    total_nights INTEGER;
    existing_record RECORD;
BEGIN
    total_days := (p_check_out - p_check_in) + 1;
    total_nights := p_check_out - p_check_in;
    price_per_day := ROUND((p_price_amount * total_nights) / total_days, 2);
    
    loop_date := p_check_in;
    
    WHILE loop_date <= p_check_out LOOP
        
        IF p_auction_id IS NOT NULL THEN
            -- TRƯỜNG HỢP MỚI: có auction_id
            -- Check conflict manually vì partial index phức tạp
            SELECT id INTO existing_record 
            FROM calendar_availability 
            WHERE property_id = p_property_id 
            AND auction_id = p_auction_id 
            AND date = loop_date;
            
            IF FOUND THEN
                -- Update existing record
                UPDATE calendar_availability 
                SET 
                    is_available = p_is_available,
                    bid_id = p_bid_id,
                    price_amount = price_per_day,
                    updated_at = CURRENT_TIMESTAMP
                WHERE property_id = p_property_id 
                AND auction_id = p_auction_id 
                AND date = loop_date;
            ELSE
                -- Insert new record
                INSERT INTO calendar_availability (
                    property_id, auction_id, date, is_available, bid_id, price_amount,
                    created_at, updated_at
                )
                VALUES (
                    p_property_id, p_auction_id, loop_date, p_is_available, p_bid_id, price_per_day,
                    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                );
            END IF;
            
        ELSE
            -- TRƯỜNG HỢP CŨ: auction_id = NULL (legacy data)
            SELECT id INTO existing_record 
            FROM calendar_availability 
            WHERE property_id = p_property_id 
            AND auction_id IS NULL 
            AND date = loop_date;
            
            IF FOUND THEN
                -- Update existing legacy record
                UPDATE calendar_availability 
                SET 
                    is_available = p_is_available,
                    bid_id = p_bid_id,
                    price_amount = price_per_day,
                    updated_at = CURRENT_TIMESTAMP
                WHERE property_id = p_property_id 
                AND auction_id IS NULL 
                AND date = loop_date;
            ELSE
                -- Insert new legacy record
                INSERT INTO calendar_availability (
                    property_id, auction_id, date, is_available, bid_id, price_amount,
                    created_at, updated_at
                )
                VALUES (
                    p_property_id, NULL, loop_date, p_is_available, p_bid_id, price_per_day,
                    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                );
            END IF;
        END IF;

        loop_date := loop_date + INTERVAL '1 day';
    END LOOP;
    
    RAISE NOTICE 'Processed % days for property %, auction %', 
                 total_days, p_property_id, COALESCE(p_auction_id::text, 'NULL');
END;
$$ LANGUAGE plpgsql;

-- Bước 4: Trigger function cập nhật
CREATE OR REPLACE FUNCTION trigger_insert_calendar_availability()
RETURNS TRIGGER AS $$
DECLARE
    bid_property_id BIGINT;
BEGIN
    -- Lấy property_id từ auction
    SELECT a.property_id INTO bid_property_id
    FROM auctions a 
    WHERE a.id = NEW.auction_id;
    
    -- Gọi function với auction_id từ bid
    PERFORM insert_calendar_availability_from_bid(
        NEW.id,                    -- bid_id
        bid_property_id,           -- property_id  
        NEW.auction_id,            -- auction_id (có thể NULL cho legacy)
        NEW.check_in,              -- check_in
        NEW.check_out,             -- check_out
        NEW.price_per_night,       -- price_per_night
        false                      -- is_available = false
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMIT;

-- -- TEST CASES để verify
--
-- -- Test 1: Data mới (có auction_id)
-- DO $$
-- BEGIN
--     PERFORM insert_calendar_availability_from_bid(
--         'bid-001'::UUID,
--         1,                                    -- property_id
--         'auction-123'::UUID,                  -- auction_id (NOT NULL)
--         '2025-08-20'::DATE,
--         '2025-08-22'::DATE,
--         1000.00,
--         false
--     );
--     RAISE NOTICE 'Test 1 (new data with auction_id): SUCCESS';
-- EXCEPTION WHEN OTHERS THEN
--     RAISE NOTICE 'Test 1 FAILED: %', SQLERRM;
-- END $$;
--
-- -- Test 2: Data cũ (auction_id = NULL)
-- DO $$
-- BEGIN
--     PERFORM insert_calendar_availability_from_bid(
--         'bid-002'::UUID,
--         2,                                    -- property_id
--         NULL,                                 -- auction_id = NULL (legacy)
--         '2025-08-20'::DATE,
--         '2025-08-22'::DATE,
--         800.00,
--         false
--     );
--     RAISE NOTICE 'Test 2 (legacy data auction_id=NULL): SUCCESS';
-- EXCEPTION WHEN OTHERS THEN
--     RAISE NOTICE 'Test 2 FAILED: %', SQLERRM;
-- END $$;
--
-- -- Test 3: Update existing record (new data)
-- DO $$
-- BEGIN
--     -- Insert same bid again (should update)
--     PERFORM insert_calendar_availability_from_bid(
--         'bid-003'::UUID,
--         1,                                    -- same property
--         'auction-123'::UUID,                  -- same auction
--         '2025-08-20'::DATE,
--         '2025-08-22'::DATE,
--         1200.00,                              -- different price
--         false
--     );
--     RAISE NOTICE 'Test 3 (update existing): SUCCESS';
-- EXCEPTION WHEN OTHERS THEN
--     RAISE NOTICE 'Test 3 FAILED: %', SQLERRM;
-- END $$;
--
-- -- Verify results
-- SELECT
--     property_id,
--     auction_id,
--     date,
--     price_amount,
--     bid_id,
--     CASE
--         WHEN auction_id IS NULL THEN 'Legacy Data'
--         ELSE 'New Data'
--     END as data_type
-- FROM calendar_availability
-- ORDER BY property_id, auction_id NULLS FIRST, date;