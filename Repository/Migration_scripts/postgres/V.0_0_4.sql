
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

BEGIN;

-- Xóa ràng buộc khóa ngoại wishlist_property_id_fkey trước khi xóa cột property_id
ALTER TABLE public.wishlist
DROP CONSTRAINT IF EXISTS wishlist_property_id_fkey;

-- Xóa cột property_id từ bảng wishlist
ALTER TABLE public.wishlist
DROP COLUMN IF EXISTS property_id;

-- Tạo bảng property_types
CREATE TABLE IF NOT EXISTS public.property_types (
    name character varying(50) PRIMARY KEY,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.property_types OWNER TO postgres;

-- Tạo bảng property_categories
CREATE TABLE IF NOT EXISTS public.property_categories (
    name character varying(50) PRIMARY KEY,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.property_categories OWNER TO postgres;

-- Đồng bộ dữ liệu property_type từ bảng properties
INSERT INTO public.property_types (name)
SELECT DISTINCT property_type
FROM public.properties
WHERE property_type IS NOT NULL
ON CONFLICT (name) DO NOTHING;

-- Đồng bộ dữ liệu category từ bảng properties
INSERT INTO public.property_categories (name)
SELECT DISTINCT category
FROM public.properties
WHERE category IS NOT NULL
ON CONFLICT (name) DO NOTHING;

-- Thêm ràng buộc khóa ngoại cho properties
ALTER TABLE public.properties
ADD CONSTRAINT fk_property_type
FOREIGN KEY (property_type)
REFERENCES public.property_types(name)
ON DELETE RESTRICT
ON UPDATE CASCADE;

ALTER TABLE public.properties
ADD CONSTRAINT fk_property_category
FOREIGN KEY (category)
REFERENCES public.property_categories(name)
ON DELETE RESTRICT
ON UPDATE CASCADE;

ALTER TABLE public.property_amenities
DROP CONSTRAINT IF EXISTS property_amenities_property_id_fkey;

ALTER TABLE public.property_amenities
ADD CONSTRAINT property_amenities_property_id_fkey 
FOREIGN KEY (property_id)
REFERENCES public.properties(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE public.notification
    -- Bỏ cột type
    DROP COLUMN IF EXISTS type,
    -- Đổi cột data thành link (text, nullable)
    DROP COLUMN IF EXISTS data,
    ADD COLUMN IF NOT EXISTS link TEXT,

ALTER TABLE subscription ALTER COLUMN endpoint TYPE TEXT;
    
COMMIT;
