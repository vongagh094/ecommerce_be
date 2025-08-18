-- Incremental Low-Risk Migration
-- Purpose: Add performance indexes and optional columns with minimal locking for large datasets
-- Notes:
-- - Uses CREATE INDEX CONCURRENTLY (cannot run inside a transaction)
-- - Avoids data type changes or default changes
-- - Adds only nullable column(s) with IF NOT EXISTS

-- Optional: Reduce lock wait to avoid long blocking (adjust as needed)
-- SET lock_timeout = '5s';
-- SET statement_timeout = '0';

-- 1) Safe column additions (nullable, guarded)
DO $$
BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM information_schema.columns
		WHERE table_schema = 'public'
		  AND table_name = 'payment_sessions'
		  AND column_name = 'order_url'
	) THEN
		ALTER TABLE public.payment_sessions ADD COLUMN order_url text;
	END IF;
END$$;

-- 2) Indexes for property_images
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_property_images_property_id ON public.property_images(property_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_property_images_is_primary ON public.property_images(property_id, is_primary);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_property_images_primary ON public.property_images(property_id) WHERE is_primary = true;

-- 3) Indexes for reviews
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_property_id ON public.reviews(property_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_reviewer_id ON public.reviews(reviewer_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_booking_id ON public.reviews(booking_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_rating ON public.reviews(rating);

-- 4) Indexes for bookings
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_bookings_guest_id ON public.bookings(guest_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_bookings_host_id ON public.bookings(host_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_bookings_dates ON public.bookings(check_in_date, check_out_date);

-- 5) Indexes for bids
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_bids_user_id ON public.bids(user_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_bids_status ON public.bids(status);

-- 6) Indexes for payments
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_payment_sessions_app_trans_id ON public.payment_sessions(app_trans_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_payment_sessions_user_auction ON public.payment_sessions(user_id, auction_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_payment_transactions_app_trans_id ON public.payment_transactions(app_trans_id);

-- 7) Existing helpful indexes (idempotent, may already exist)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_auctions_window ON public.auctions (start_date, end_date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_bids_date_range ON public.bids (check_in, check_out);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_calendar_prop_date ON public.calendar_availability (property_id, date);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_properties_location ON public.properties (city, state, country);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON public.users (email); 