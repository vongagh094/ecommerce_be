-- Unified Database Schema for ecommerce_be
-- Combines base schema with payment tables and performance indexes
-- Safe to run multiple times due to IF NOT EXISTS guards where applicable

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

-- Types
DO $$ BEGIN
	IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'auction_objective') THEN
		CREATE TYPE public.auction_objective AS ENUM (
			'HIGHEST_TOTAL',
			'HIGHEST_PER_NIGHT',
			'HYBRID'
		);
	END IF;
END $$;

DO $$ BEGIN
	IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_status') THEN
		CREATE TYPE public.offer_status AS ENUM (
			'WAITING',
			'ACCEPTED',
			'DECLINED',
			'EXPIRED'
		);
	END IF;
END $$;

-- Functions
CREATE OR REPLACE FUNCTION public.update_updated_at_column() RETURNS trigger
	LANGUAGE plpgsql
AS $$
BEGIN
	NEW.updated_at = CURRENT_TIMESTAMP;
	RETURN NEW;
END;
$$;

-- Tables
CREATE TABLE IF NOT EXISTS public.amenities (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	name text NOT NULL,
	category text NOT NULL,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.auctions (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	property_id bigint NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	min_nights integer DEFAULT 1,
	max_nights integer,
	starting_price numeric(10,2) NOT NULL,
	current_highest_bid numeric(10,2),
	bid_increment numeric(10,2) DEFAULT 1.00,
	minimum_bid numeric(10,2) NOT NULL,
	auction_start_time timestamp WITHOUT TIME ZONE NOT NULL,
	auction_end_time timestamp WITHOUT TIME ZONE NOT NULL,
	objective public.auction_objective DEFAULT 'HIGHEST_TOTAL',
	status varchar(50) DEFAULT 'PENDING',
	winner_user_id bigint,
	total_bids integer DEFAULT 0,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_auction_prices CHECK (starting_price > 0 AND minimum_bid > 0 AND bid_increment > 0),
	CONSTRAINT chk_auction_times CHECK (auction_end_time > auction_start_time),
	CONSTRAINT chk_auction_window CHECK (end_date > start_date)
);

CREATE TABLE IF NOT EXISTS public.banners (
	banner_id bigint PRIMARY KEY,
	banner_title varchar(255) NOT NULL,
	banner_img varchar(255),
	is_active boolean DEFAULT true,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sequences
CREATE SEQUENCE IF NOT EXISTS public.banners_banner_id_seq OWNED BY public.banners.banner_id;
ALTER TABLE IF EXISTS public.banners ALTER COLUMN banner_id SET DEFAULT nextval('public.banners_banner_id_seq');

CREATE TABLE IF NOT EXISTS public.bid_events (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	auction_id uuid NOT NULL,
	event_type varchar(50) NOT NULL,
	user_id bigint,
	bid_id uuid,
	event_data jsonb,
	event_time timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.bid_notifications (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	user_id bigint NOT NULL,
	bid_id uuid,
	message text NOT NULL,
	sent_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	is_read boolean DEFAULT false
);

CREATE TABLE IF NOT EXISTS public.bids (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	auction_id uuid NOT NULL,
	user_id bigint NOT NULL,
	check_in date NOT NULL,
	check_out date NOT NULL,
	nights integer GENERATED ALWAYS AS (GREATEST(1, (check_out - check_in))) STORED,
	total_amount numeric(10,2) NOT NULL,
	price_per_night numeric(10,2) GENERATED ALWAYS AS (total_amount / (GREATEST(1, (check_out - check_in)))::numeric) STORED,
	allow_partial boolean DEFAULT true,
	partial_awarded boolean DEFAULT false,
	bid_time timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	status varchar(50) DEFAULT 'ACTIVE',
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_bid_dates CHECK (check_out > check_in)
);

CREATE TABLE IF NOT EXISTS public.bookings (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	auction_id uuid,
	property_id bigint NOT NULL,
	guest_id bigint NOT NULL,
	host_id bigint NOT NULL,
	check_in_date date NOT NULL,
	check_out_date date NOT NULL,
	total_nights integer NOT NULL,
	base_amount numeric(10,2) NOT NULL,
	cleaning_fee numeric(10,2) DEFAULT 0,
	taxes numeric(10,2) DEFAULT 0,
	total_amount numeric(10,2) NOT NULL,
	booking_status varchar(50) DEFAULT 'PENDING',
	payment_status varchar(50) DEFAULT 'PENDING',
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_booking_dates CHECK (check_out_date > check_in_date)
);

CREATE TABLE IF NOT EXISTS public.calendar_availability (
	id bigint PRIMARY KEY,
	property_id bigint NOT NULL,
	date date NOT NULL,
	is_available boolean DEFAULT true,
	bid_id uuid,
	price_amount numeric(10,2),
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.calendar_availability_id_seq OWNED BY public.calendar_availability.id;
ALTER TABLE IF EXISTS public.calendar_availability ALTER COLUMN id SET DEFAULT nextval('public.calendar_availability_id_seq');

CREATE TABLE IF NOT EXISTS public.configuration (
	id bigint PRIMARY KEY,
	commission_rate numeric(5,2) NOT NULL,
	hybrid_objective_weight numeric(5,2) DEFAULT 0.5,
	website_name varchar(100) NOT NULL,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_commission_rate CHECK (commission_rate >= 0 AND commission_rate <= 100)
);
CREATE SEQUENCE IF NOT EXISTS public.configuration_id_seq OWNED BY public.configuration.id;
ALTER TABLE IF EXISTS public.configuration ALTER COLUMN id SET DEFAULT nextval('public.configuration_id_seq');

CREATE TABLE IF NOT EXISTS public.conversation (
	id bigint PRIMARY KEY,
	property_id bigint,
	guest_id bigint NOT NULL,
	host_id bigint NOT NULL,
	last_message_at timestamp WITHOUT TIME ZONE,
	is_archived boolean DEFAULT false,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.conversation_id_seq OWNED BY public.conversation.id;
ALTER TABLE IF EXISTS public.conversation ALTER COLUMN id SET DEFAULT nextval('public.conversation_id_seq');

CREATE TABLE IF NOT EXISTS public.house_rules (
	id bigint PRIMARY KEY,
	property_id bigint NOT NULL,
	rule_type varchar(50) DEFAULT 'general',
	title varchar(255),
	description text,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.house_rules_id_seq OWNED BY public.house_rules.id;
ALTER TABLE IF EXISTS public.house_rules ALTER COLUMN id SET DEFAULT nextval('public.house_rules_id_seq');

CREATE TABLE IF NOT EXISTS public.location_descriptions (
	id bigint PRIMARY KEY,
	property_id bigint NOT NULL,
	description_type varchar(50) DEFAULT 'general',
	title varchar(255),
	description text,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.location_descriptions_id_seq OWNED BY public.location_descriptions.id;
ALTER TABLE IF EXISTS public.location_descriptions ALTER COLUMN id SET DEFAULT nextval('public.location_descriptions_id_seq');

CREATE TABLE IF NOT EXISTS public.message (
	id bigint PRIMARY KEY,
	conversation_id bigint NOT NULL,
	sender_id bigint NOT NULL,
	message_text text,
	sent_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	is_read boolean DEFAULT false
);
CREATE SEQUENCE IF NOT EXISTS public.message_id_seq OWNED BY public.message.id;
ALTER TABLE IF EXISTS public.message ALTER COLUMN id SET DEFAULT nextval('public.message_id_seq');

CREATE TABLE IF NOT EXISTS public.notification (
	id bigint PRIMARY KEY,
	user_id bigint,
	type varchar(50),
	title varchar(255) NOT NULL,
	message text NOT NULL,
	data jsonb,
	is_read boolean DEFAULT false,
	is_pushed boolean DEFAULT false,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.notification_id_seq OWNED BY public.notification.id;
ALTER TABLE IF EXISTS public.notification ALTER COLUMN id SET DEFAULT nextval('public.notification_id_seq');

CREATE TABLE IF NOT EXISTS public.properties (
	id bigint PRIMARY KEY,
	host_id bigint NOT NULL,
	title varchar(255) NOT NULL,
	description text,
	property_type varchar(50) NOT NULL,
	category varchar(50) NOT NULL,
	max_guests integer NOT NULL,
	bedrooms integer,
	bathrooms integer,
	address_line1 varchar(255),
	city varchar(100),
	state varchar(100),
	country varchar(100),
	postal_code varchar(20),
	latitude numeric(10,8),
	longitude numeric(11,8),
	base_price numeric(10,2) NOT NULL,
	cleaning_fee numeric(10,2) DEFAULT 0,
	cancellation_policy varchar(50) NOT NULL,
	instant_book boolean DEFAULT false,
	minimum_stay integer DEFAULT 1,
	home_tier integer,
	is_guest_favorite boolean,
	language varchar(10) DEFAULT 'en',
	status varchar(50) DEFAULT 'DRAFT',
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_coordinates CHECK (((latitude IS NULL AND longitude IS NULL) OR ((latitude >= -90 AND latitude <= 90) AND (longitude >= -180 AND longitude <= 180)))),
	CONSTRAINT chk_guest_capacity CHECK (max_guests > 0),
	CONSTRAINT chk_prices CHECK (base_price > 0)
);
CREATE SEQUENCE IF NOT EXISTS public.properties_id_seq OWNED BY public.properties.id;
ALTER TABLE IF EXISTS public.properties ALTER COLUMN id SET DEFAULT nextval('public.properties_id_seq');

CREATE TABLE IF NOT EXISTS public.property_amenities (
	property_id bigint NOT NULL,
	amenity_id uuid NOT NULL,
	PRIMARY KEY (property_id, amenity_id)
);

CREATE TABLE IF NOT EXISTS public.property_highlights (
	id bigint PRIMARY KEY,
	property_id bigint NOT NULL,
	title varchar(255),
	subtitle varchar(255),
	icon varchar(100),
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.property_highlights_id_seq OWNED BY public.property_highlights.id;
ALTER TABLE IF EXISTS public.property_highlights ALTER COLUMN id SET DEFAULT nextval('public.property_highlights_id_seq');

CREATE TABLE IF NOT EXISTS public.property_images (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	property_id bigint NOT NULL,
	image_url text NOT NULL,
	alt_text varchar(255),
	title varchar(255),
	display_order integer DEFAULT 0,
	is_primary boolean DEFAULT false,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.reports (
	report_id bigint PRIMARY KEY,
	property_id bigint NOT NULL,
	user_id bigint NOT NULL,
	report_reason varchar(255) NOT NULL,
	report_status varchar(50) DEFAULT 'pending',
	report_reply varchar(255),
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.reports_report_id_seq OWNED BY public.reports.report_id;
ALTER TABLE IF EXISTS public.reports ALTER COLUMN report_id SET DEFAULT nextval('public.reports_report_id_seq');

CREATE TABLE IF NOT EXISTS public.reviews (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	booking_id uuid,
	reviewer_id bigint NOT NULL,
	reviewee_id bigint NOT NULL,
	property_id bigint NOT NULL,
	rating numeric(3,2) NOT NULL,
	review_text text,
	review_type varchar(50) NOT NULL,
	response_text text,
	is_visible boolean DEFAULT true,
	accuracy_rating numeric(3,2),
	checking_rating numeric(3,2),
	cleanliness_rating numeric(3,2),
	communication_rating numeric(3,2),
	location_rating numeric(3,2),
	value_rating numeric(3,2),
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_rating CHECK (rating >= 1 AND rating <= 5)
);

CREATE TABLE IF NOT EXISTS public.second_chance_offers (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	bid_id uuid NOT NULL,
	offered_check_in date NOT NULL,
	offered_check_out date NOT NULL,
	response_deadline timestamp WITHOUT TIME ZONE NOT NULL,
	status public.offer_status DEFAULT 'WAITING',
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	responded_at timestamp WITHOUT TIME ZONE
);

CREATE TABLE IF NOT EXISTS public.subscription (
	id bigint PRIMARY KEY,
	endpoint varchar(255) NOT NULL,
	p256dh varchar(255) NOT NULL,
	auth varchar(255) NOT NULL,
	user_id bigint NOT NULL
);
CREATE SEQUENCE IF NOT EXISTS public.subscription_id_seq OWNED BY public.subscription.id;
ALTER TABLE IF EXISTS public.subscription ALTER COLUMN id SET DEFAULT nextval('public.subscription_id_seq');

CREATE TABLE IF NOT EXISTS public.systemlogs (
	id bigint PRIMARY KEY,
	type varchar(100) NOT NULL,
	status varchar(50) NOT NULL,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.systemlogs_id_seq OWNED BY public.systemlogs.id;
ALTER TABLE IF EXISTS public.systemlogs ALTER COLUMN id SET DEFAULT nextval('public.systemlogs_id_seq');

CREATE TABLE IF NOT EXISTS public.users (
	id bigint PRIMARY KEY,
	email varchar(255) NOT NULL,
	username varchar(255) NOT NULL,
	password_hash varchar(255),
	full_name varchar(255) NOT NULL,
	first_name varchar(255),
	last_name varchar(255),
	profile_image_url text,
	verification_status varchar(50),
	is_active boolean DEFAULT true,
	is_super_host boolean DEFAULT false,
	host_about text,
	host_review_count integer,
	host_rating_average numeric(3,2),
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT users_email_format CHECK ((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);
CREATE SEQUENCE IF NOT EXISTS public.users_id_seq OWNED BY public.users.id;
ALTER TABLE IF EXISTS public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq');

CREATE TABLE IF NOT EXISTS public.wishlist (
	id integer PRIMARY KEY,
	user_id integer NOT NULL,
	property_id integer NOT NULL,
	is_private boolean DEFAULT false,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE SEQUENCE IF NOT EXISTS public.wishlist_id_seq AS integer OWNED BY public.wishlist.id;
ALTER TABLE IF EXISTS public.wishlist ALTER COLUMN id SET DEFAULT nextval('public.wishlist_id_seq');

CREATE TABLE IF NOT EXISTS public.wishlist_property (
	wishlist_id bigint NOT NULL,
	property_id bigint NOT NULL,
	added_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (wishlist_id, property_id)
);

-- Payment tables (unified)
CREATE TABLE IF NOT EXISTS public.payment_sessions (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	user_id bigint NOT NULL,
	auction_id uuid NOT NULL,
	bid_id uuid NOT NULL,
	app_trans_id varchar(64) NOT NULL UNIQUE,
	amount numeric(10,2) NOT NULL,
	selected_nights jsonb NOT NULL,
	status varchar(50) NOT NULL DEFAULT 'PENDING',
	idempotency_key varchar(128) UNIQUE,
	expires_at timestamp WITHOUT TIME ZONE,
	order_url text,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.payment_transactions (
	id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
	session_id uuid NOT NULL REFERENCES public.payment_sessions(id) ON DELETE CASCADE,
	app_trans_id varchar(64) NOT NULL,
	zp_trans_id varchar(64),
	amount numeric(10,2) NOT NULL,
	status varchar(50) NOT NULL DEFAULT 'PENDING',
	paid_at timestamp WITHOUT TIME ZONE,
	raw jsonb,
	created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Constraints
ALTER TABLE IF EXISTS public.auctions
	ADD CONSTRAINT IF NOT EXISTS auctions_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.auctions
	ADD CONSTRAINT IF NOT EXISTS auctions_winner_user_id_fkey FOREIGN KEY (winner_user_id) REFERENCES public.users(id) ON DELETE SET NULL;

ALTER TABLE IF EXISTS public.bids
	ADD CONSTRAINT IF NOT EXISTS bids_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.bids
	ADD CONSTRAINT IF NOT EXISTS bids_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.bookings
	ADD CONSTRAINT IF NOT EXISTS bookings_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id) ON DELETE SET NULL;
ALTER TABLE IF EXISTS public.bookings
	ADD CONSTRAINT IF NOT EXISTS bookings_guest_id_fkey FOREIGN KEY (guest_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.bookings
	ADD CONSTRAINT IF NOT EXISTS bookings_host_id_fkey FOREIGN KEY (host_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.bookings
	ADD CONSTRAINT IF NOT EXISTS bookings_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.calendar_availability
	ADD CONSTRAINT IF NOT EXISTS calendar_availability_property_id_date_key UNIQUE (property_id, date);
ALTER TABLE IF EXISTS public.calendar_availability
	ADD CONSTRAINT IF NOT EXISTS calendar_availability_bid_id_fkey FOREIGN KEY (bid_id) REFERENCES public.bids(id) ON DELETE SET NULL;
ALTER TABLE IF EXISTS public.calendar_availability
	ADD CONSTRAINT IF NOT EXISTS calendar_availability_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.property_amenities
	ADD CONSTRAINT IF NOT EXISTS property_amenities_amenity_id_fkey FOREIGN KEY (amenity_id) REFERENCES public.amenities(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.property_amenities
	ADD CONSTRAINT IF NOT EXISTS property_amenities_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.property_highlights
	ADD CONSTRAINT IF NOT EXISTS property_highlights_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.property_images
	ADD CONSTRAINT IF NOT EXISTS property_images_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.reviews
	ADD CONSTRAINT IF NOT EXISTS reviews_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.bookings(id) ON DELETE SET NULL;
ALTER TABLE IF EXISTS public.reviews
	ADD CONSTRAINT IF NOT EXISTS reviews_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.reviews
	ADD CONSTRAINT IF NOT EXISTS reviews_reviewee_id_fkey FOREIGN KEY (reviewee_id) REFERENCES public.users(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.reviews
	ADD CONSTRAINT IF NOT EXISTS reviews_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES public.users(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.properties
	ADD CONSTRAINT IF NOT EXISTS properties_host_id_fkey FOREIGN KEY (host_id) REFERENCES public.users(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.wishlist
	ADD CONSTRAINT IF NOT EXISTS wishlist_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.wishlist
	ADD CONSTRAINT IF NOT EXISTS wishlist_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;

-- Payment FKs
ALTER TABLE IF EXISTS public.payment_sessions
	ADD CONSTRAINT IF NOT EXISTS fk_payment_sessions_auction_id FOREIGN KEY (auction_id) REFERENCES public.auctions(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.payment_sessions
	ADD CONSTRAINT IF NOT EXISTS fk_payment_sessions_bid_id FOREIGN KEY (bid_id) REFERENCES public.bids(id) ON DELETE CASCADE;
ALTER TABLE IF EXISTS public.payment_sessions
	ADD CONSTRAINT IF NOT EXISTS fk_payment_sessions_user_id FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;

-- Indexes (existing + performance additions)
CREATE INDEX IF NOT EXISTS idx_auctions_window ON public.auctions (start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_bids_date_range ON public.bids (check_in, check_out);
CREATE INDEX IF NOT EXISTS idx_calendar_prop_date ON public.calendar_availability (property_id, date);
CREATE INDEX IF NOT EXISTS idx_properties_location ON public.properties (city, state, country);
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users (email);

-- Property images performance indexes
CREATE INDEX IF NOT EXISTS idx_property_images_property_id ON public.property_images(property_id);
CREATE INDEX IF NOT EXISTS idx_property_images_is_primary ON public.property_images(property_id, is_primary);
CREATE INDEX IF NOT EXISTS idx_property_images_primary ON public.property_images(property_id) WHERE is_primary = true;

-- Reviews performance indexes
CREATE INDEX IF NOT EXISTS idx_reviews_property_id ON public.reviews(property_id);
CREATE INDEX IF NOT EXISTS idx_reviews_reviewer_id ON public.reviews(reviewer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_booking_id ON public.reviews(booking_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON public.reviews(rating);

-- Bookings performance indexes
CREATE INDEX IF NOT EXISTS idx_bookings_guest_id ON public.bookings(guest_id);
CREATE INDEX IF NOT EXISTS idx_bookings_host_id ON public.bookings(host_id);
CREATE INDEX IF NOT EXISTS idx_bookings_dates ON public.bookings(check_in_date, check_out_date);

-- Bids performance indexes
CREATE INDEX IF NOT EXISTS idx_bids_user_id ON public.bids(user_id);
CREATE INDEX IF NOT EXISTS idx_bids_status ON public.bids(status);

-- Payments indexes
CREATE INDEX IF NOT EXISTS idx_payment_sessions_app_trans_id ON public.payment_sessions(app_trans_id);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_app_trans_id ON public.payment_transactions(app_trans_id);
CREATE INDEX IF NOT EXISTS idx_payment_sessions_user_auction ON public.payment_sessions(user_id, auction_id);

-- Triggers to keep updated_at fresh
DO $$ BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM pg_trigger WHERE tgname = 'trg_auctions_upd'
	) THEN
		CREATE TRIGGER trg_auctions_upd BEFORE UPDATE ON public.auctions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
	END IF;
END $$;

DO $$ BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM pg_trigger WHERE tgname = 'trg_bookings_upd'
	) THEN
		CREATE TRIGGER trg_bookings_upd BEFORE UPDATE ON public.bookings FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
	END IF;
END $$;

DO $$ BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM pg_trigger WHERE tgname = 'trg_props_upd'
	) THEN
		CREATE TRIGGER trg_props_upd BEFORE UPDATE ON public.properties FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
	END IF;
END $$;

DO $$ BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM pg_trigger WHERE tgname = 'trg_reviews_upd'
	) THEN
		CREATE TRIGGER trg_reviews_upd BEFORE UPDATE ON public.reviews FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
	END IF;
END $$;

DO $$ BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM pg_trigger WHERE tgname = 'trg_users_upd'
	) THEN
		CREATE TRIGGER trg_users_upd BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
	END IF;
END $$;

-- Payment triggers
DO $$ BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM pg_trigger WHERE tgname = 'trg_payment_sessions_upd'
	) THEN
		CREATE TRIGGER trg_payment_sessions_upd BEFORE UPDATE ON public.payment_sessions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
	END IF;
END $$;

DO $$ BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM pg_trigger WHERE tgname = 'trg_payment_transactions_upd'
	) THEN
		CREATE TRIGGER trg_payment_transactions_upd BEFORE UPDATE ON public.payment_transactions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
	END IF;
END $$;

-- Unique constraints
ALTER TABLE IF EXISTS public.users ADD CONSTRAINT IF NOT EXISTS users_email_key UNIQUE (email);
ALTER TABLE IF EXISTS public.users ADD CONSTRAINT IF NOT EXISTS users_username_key UNIQUE (username); 