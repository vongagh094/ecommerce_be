CREATE OR REPLACE FUNCTION get_calendar_optimized_direct(
    p_property_id BIGINT,
    p_year INTEGER,
    p_month INTEGER
)
RETURNS TABLE (
    date DATE,
    highest_bid NUMERIC(10,2),
    active_bids INTEGER,
    minimum_to_win NUMERIC(10,2),
    base_price NUMERIC(10,2),
    demand_level TEXT,
    success_rate INTEGER,
    is_available BOOLEAN,
    is_booked BOOLEAN
) AS $$
DECLARE
    month_start DATE := make_date(p_year, p_month, 1);
    month_end DATE := month_start + interval '1 month' - interval '1 day';
    v_base_price NUMERIC(10,2);
BEGIN
    -- Get base price
    SELECT p.base_price INTO v_base_price
    FROM properties p WHERE p.id = p_property_id;

    RETURN QUERY
    WITH daily_bids AS (
        -- Tính số active bids cho mỗi ngày cụ thể
        SELECT
            d.date_val::date as target_date,
            COUNT(DISTINCT b.id)::INTEGER as active_bids_count,
            COALESCE(MAX(b.total_amount / NULLIF(b.nights, 0)), 0)::NUMERIC(10,2) as highest_bid_per_night
        FROM generate_series(month_start, month_end, '1 day') d(date_val)
        LEFT JOIN auctions a ON (
            a.property_id = p_property_id
            AND a.start_date <= d.date_val::date
            AND a.end_date > d.date_val::date
            AND a.status IN ('ACTIVE', 'COMPLETED')
        )
        LEFT JOIN bids b ON (
            b.auction_id = a.id
            AND b.status = 'ACTIVE'
            AND b.check_in <= d.date_val::date
            AND b.check_out > d.date_val::date
        )
        GROUP BY d.date_val
    )
    SELECT
        db.target_date,
        CASE
            WHEN db.highest_bid_per_night > 0 THEN db.highest_bid_per_night
            ELSE v_base_price
        END as highest_bid,
        COALESCE(db.active_bids_count, 0) as active_bids,
        CASE
            WHEN db.highest_bid_per_night > 0 THEN db.highest_bid_per_night + 10::NUMERIC(10,2)
            ELSE v_base_price + 10::NUMERIC(10,2)
        END as minimum_to_win,
        v_base_price as base_price,
        CASE
            WHEN COALESCE(db.active_bids_count, 0) <= 3 THEN 'low'::TEXT
            WHEN COALESCE(db.active_bids_count, 0) > 10 THEN 'high'::TEXT
            ELSE 'moderate'::TEXT
        END as demand_level,
        CASE
            WHEN COALESCE(db.active_bids_count, 0) <= 3 THEN 85
            WHEN COALESCE(db.active_bids_count, 0) > 10 THEN 40
            ELSE 65
        END as success_rate,
        COALESCE(ca.is_available, TRUE) as is_available,
        (b.property_id IS NOT NULL OR ca.bid_id IS NOT NULL) as is_booked

    FROM daily_bids db
    LEFT JOIN calendar_availability ca ON (
        ca.property_id = p_property_id AND ca.date = db.target_date
    )
    LEFT JOIN bookings b ON (
        b.property_id = p_property_id
        AND b.check_in_date <= db.target_date
        AND b.check_out_date > db.target_date
        AND b.booking_status = 'CONFIRMED'
    )
    ORDER BY db.target_date;
END;
$$ LANGUAGE plpgsql STABLE;