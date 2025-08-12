
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
    prop_base_price INTEGER;
BEGIN
    -- Get base price
    SELECT base_price::INTEGER INTO prop_base_price
    FROM properties WHERE id = p_property_id;

    RETURN QUERY
    SELECT
        d.date_val::date,
        COALESCE(a.current_highest_bid::INTEGER, prop_base_price),
        COALESCE(a.total_bids, 0),
        COALESCE(a.current_highest_bid::INTEGER, prop_base_price) + 10,
        prop_base_price,
        CASE
            WHEN COALESCE(a.total_bids, 0) <= 3 THEN 'low'::TEXT
            WHEN COALESCE(a.total_bids, 0) > 10 THEN 'high'::TEXT
            ELSE 'moderate'::TEXT
        END,
        CASE
            WHEN COALESCE(a.total_bids, 0) <= 3 THEN 85
            WHEN COALESCE(a.total_bids, 0) > 10 THEN 40
            ELSE 65
        END,
        COALESCE(ca.is_available, TRUE),
        (b.property_id IS NOT NULL OR ca.bid_id IS NOT NULL)

    FROM generate_series(month_start, month_end, '1 day') d(date_val)
    LEFT JOIN auctions a ON (
        a.property_id = p_property_id
        AND a.start_date <= d.date_val::date
        AND a.end_date > d.date_val::date
        AND a.status IN ('ACTIVE', 'COMPLETED')
    )
    LEFT JOIN calendar_availability ca ON (
        ca.property_id = p_property_id AND ca.date = d.date_val::date
    )
    LEFT JOIN bookings b ON (
        b.property_id = p_property_id
        AND b.check_in_date <= d.date_val::date
        AND b.check_out_date > d.date_val::date
        AND b.booking_status = 'CONFIRMED'
    )
    ORDER BY d.date_val;
END;
$$ LANGUAGE plpgsql STABLE;

