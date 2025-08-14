CREATE OR REPLACE FUNCTION insert_calendar_availability_from_bid(
    p_bid_id UUID,
    p_property_id BIGINT,
    p_check_in DATE,
    p_check_out DATE,
    p_price_amount NUMERIC(10,2) DEFAULT NULL,
    p_is_available BOOLEAN DEFAULT false
)
RETURNS VOID AS $$
DECLARE
    loop_date DATE;
BEGIN
    -- Validate input dates
    IF p_check_out <= p_check_in THEN
        RAISE EXCEPTION 'Check-out date must be after check-in date';
    END IF;

    -- Loop through each date from check_in to check_out (exclusive)
    loop_date := p_check_in;

    WHILE loop_date < p_check_out LOOP
        -- Insert or update calendar availability for each date
        INSERT INTO calendar_availability (
            property_id,
            date,
            is_available,
            bid_id,
            price_amount,
            created_at,
            updated_at
        )
        VALUES (
            p_property_id,
            current_date,
            p_is_available,
            p_bid_id,
            p_price_amount,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )
        ON CONFLICT (property_id, date)
        DO UPDATE SET
            is_available = EXCLUDED.is_available,
            bid_id = EXCLUDED.bid_id,
            price_amount = EXCLUDED.price_amount,
            updated_at = CURRENT_TIMESTAMP;

        -- Move to next date
        loop_date := loop_date + INTERVAL '1 day';
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Trigger function để tự động insert calendar availability khi có bid mới
CREATE OR REPLACE FUNCTION trigger_insert_calendar_availability()
RETURNS TRIGGER AS $$
DECLARE
    bid_property_id BIGINT;
    bid_price_per_night NUMERIC(10,2);
BEGIN
    -- Lấy property_id từ auction
    SELECT a.property_id INTO bid_property_id
    FROM auctions a
    WHERE a.id = NEW.auction_id;

    -- Tính price per night từ bid
    bid_price_per_night := NEW.price_per_night;

    -- Insert calendar availability cho bid này
    PERFORM insert_calendar_availability_from_bid(
        NEW.id,
        bid_property_id,
        NEW.check_in,
        NEW.check_out,
        bid_price_per_night,
        false -- Đánh dấu là không available vì đã có bid
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tạo trigger để tự động chạy khi có bid mới
CREATE TRIGGER after_bid_insert_calendar
    AFTER INSERT ON bids
    FOR EACH ROW
    EXECUTE FUNCTION trigger_insert_calendar_availability();

-- Example usage:
SELECT insert_calendar_availability_from_bid(
    'd3e0d9bf-f9cc-4ddc-95ec-544c3f9fcee7'::UUID,
    11798::BIGINT,
    '2025-08-21'::DATE,
    '2025-08-24'::DATE,
    150.00::NUMERIC(10,2),
    false::BOOLEAN
);
SELECT *
FROM calendar_availability
WHERE bid_id = 'd3e0d9bf-f9cc-4ddc-95ec-544c3f9fcee7'::UUID;