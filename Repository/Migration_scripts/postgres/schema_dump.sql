--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Debian 14.18-1.pgdg120+1)
-- Dumped by pg_dump version 14.18 (Debian 14.18-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: auction_objective; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.auction_objective AS ENUM (
    'HIGHEST_TOTAL',
    'HIGHEST_PER_NIGHT',
    'HYBRID'
);


ALTER TYPE public.auction_objective OWNER TO postgres;

--
-- Name: offer_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.offer_status AS ENUM (
    'WAITING',
    'ACCEPTED',
    'DECLINED',
    'EXPIRED'
);


ALTER TYPE public.offer_status OWNER TO postgres;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: amenities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amenities (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text NOT NULL,
    category text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.amenities OWNER TO postgres;

--
-- Name: auctions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auctions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    property_id bigint NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    min_nights integer DEFAULT 1,
    max_nights integer,
    starting_price numeric(10,2) NOT NULL,
    current_highest_bid numeric(10,2),
    bid_increment numeric(10,2) DEFAULT 1.00,
    minimum_bid numeric(10,2) NOT NULL,
    auction_start_time timestamp without time zone NOT NULL,
    auction_end_time timestamp without time zone NOT NULL,
    objective public.auction_objective DEFAULT 'HIGHEST_TOTAL'::public.auction_objective,
    status character varying(50) DEFAULT 'PENDING'::character varying,
    winner_user_id bigint,
    total_bids integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_auction_prices CHECK (((starting_price > (0)::numeric) AND (minimum_bid > (0)::numeric) AND (bid_increment > (0)::numeric))),
    CONSTRAINT chk_auction_times CHECK ((auction_end_time > auction_start_time)),
    CONSTRAINT chk_auction_window CHECK ((end_date > start_date))
);


ALTER TABLE public.auctions OWNER TO postgres;

--
-- Name: banners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.banners (
    banner_id bigint NOT NULL,
    banner_title character varying(255) NOT NULL,
    banner_img character varying(255),
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.banners OWNER TO postgres;

--
-- Name: banners_banner_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.banners_banner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.banners_banner_id_seq OWNER TO postgres;

--
-- Name: banners_banner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.banners_banner_id_seq OWNED BY public.banners.banner_id;


--
-- Name: bid_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bid_events (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    auction_id uuid NOT NULL,
    event_type character varying(50) NOT NULL,
    user_id bigint,
    bid_id uuid,
    event_data jsonb,
    event_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.bid_events OWNER TO postgres;

--
-- Name: bid_notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bid_notifications (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id bigint NOT NULL,
    bid_id uuid,
    message text NOT NULL,
    sent_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_read boolean DEFAULT false
);


ALTER TABLE public.bid_notifications OWNER TO postgres;

--
-- Name: bids; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bids (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    auction_id uuid NOT NULL,
    user_id bigint NOT NULL,
    check_in date NOT NULL,
    check_out date NOT NULL,
    nights integer GENERATED ALWAYS AS (GREATEST(1, (check_out - check_in))) STORED,
    total_amount numeric(10,2) NOT NULL,
    price_per_night numeric(10,2) GENERATED ALWAYS AS ((total_amount / (GREATEST(1, (check_out - check_in)))::numeric)) STORED,
    allow_partial boolean DEFAULT true,
    partial_awarded boolean DEFAULT false,
    bid_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50) DEFAULT 'ACTIVE'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_bid_dates CHECK ((check_out > check_in))
);


ALTER TABLE public.bids OWNER TO postgres;

--
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
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
    booking_status character varying(50) DEFAULT 'PENDING'::character varying,
    payment_status character varying(50) DEFAULT 'PENDING'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_booking_dates CHECK ((check_out_date > check_in_date))
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- Name: calendar_availability; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calendar_availability (
    id bigint NOT NULL,
    property_id bigint NOT NULL,
    date date NOT NULL,
    is_available boolean DEFAULT true,
    bid_id uuid,
    price_amount numeric(10,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.calendar_availability OWNER TO postgres;

--
-- Name: calendar_availability_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.calendar_availability_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendar_availability_id_seq OWNER TO postgres;

--
-- Name: calendar_availability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.calendar_availability_id_seq OWNED BY public.calendar_availability.id;


--
-- Name: configuration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.configuration (
    id bigint NOT NULL,
    commission_rate numeric(5,2) NOT NULL,
    hybrid_objective_weight numeric(5,2) DEFAULT 0.5,
    website_name character varying(100) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_commission_rate CHECK (((commission_rate >= (0)::numeric) AND (commission_rate <= (100)::numeric)))
);


ALTER TABLE public.configuration OWNER TO postgres;

--
-- Name: configuration_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.configuration_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.configuration_id_seq OWNER TO postgres;

--
-- Name: configuration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.configuration_id_seq OWNED BY public.configuration.id;


--
-- Name: conversation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conversation (
    id bigint NOT NULL,
    property_id bigint,
    guest_id bigint NOT NULL,
    host_id bigint NOT NULL,
    last_message_at timestamp without time zone,
    is_archived boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.conversation OWNER TO postgres;

--
-- Name: conversation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.conversation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.conversation_id_seq OWNER TO postgres;

--
-- Name: conversation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.conversation_id_seq OWNED BY public.conversation.id;


--
-- Name: house_rules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.house_rules (
    id bigint NOT NULL,
    property_id bigint NOT NULL,
    rule_type character varying(50) DEFAULT 'general'::character varying,
    title character varying(255),
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.house_rules OWNER TO postgres;

--
-- Name: house_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.house_rules_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.house_rules_id_seq OWNER TO postgres;

--
-- Name: house_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.house_rules_id_seq OWNED BY public.house_rules.id;


--
-- Name: location_descriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location_descriptions (
    id bigint NOT NULL,
    property_id bigint NOT NULL,
    description_type character varying(50) DEFAULT 'general'::character varying,
    title character varying(255),
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.location_descriptions OWNER TO postgres;

--
-- Name: location_descriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.location_descriptions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.location_descriptions_id_seq OWNER TO postgres;

--
-- Name: location_descriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.location_descriptions_id_seq OWNED BY public.location_descriptions.id;


--
-- Name: message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message (
    id bigint NOT NULL,
    conversation_id bigint NOT NULL,
    sender_id bigint NOT NULL,
    message_text text,
    sent_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_read boolean DEFAULT false
);


ALTER TABLE public.message OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_id_seq OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_id_seq OWNED BY public.message.id;


--
-- Name: notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification (
    id bigint NOT NULL,
    user_id bigint,
    type character varying(50),
    title character varying(255) NOT NULL,
    message text NOT NULL,
    data jsonb,
    is_read boolean DEFAULT false,
    is_pushed boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.notification OWNER TO postgres;

--
-- Name: notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_id_seq OWNER TO postgres;

--
-- Name: notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notification_id_seq OWNED BY public.notification.id;


--
-- Name: properties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.properties (
    id bigint NOT NULL,
    host_id bigint NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    property_type character varying(50) NOT NULL,
    category character varying(50) NOT NULL,
    max_guests integer NOT NULL,
    bedrooms integer,
    bathrooms integer,
    address_line1 character varying(255),
    city character varying(100),
    state character varying(100),
    country character varying(100),
    postal_code character varying(20),
    latitude numeric(10,8),
    longitude numeric(11,8),
    base_price numeric(10,2) NOT NULL,
    cleaning_fee numeric(10,2) DEFAULT 0,
    cancellation_policy character varying(50) NOT NULL,
    instant_book boolean DEFAULT false,
    minimum_stay integer DEFAULT 1,
    home_tier integer,
    is_guest_favorite boolean,
    language character varying(10) DEFAULT 'en'::character varying,
    status character varying(50) DEFAULT 'DRAFT'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_coordinates CHECK ((((latitude IS NULL) AND (longitude IS NULL)) OR (((latitude >= ('-90'::integer)::numeric) AND (latitude <= (90)::numeric)) AND ((longitude >= ('-180'::integer)::numeric) AND (longitude <= (180)::numeric))))),
    CONSTRAINT chk_guest_capacity CHECK ((max_guests > 0)),
    CONSTRAINT chk_prices CHECK ((base_price > (0)::numeric))
);


ALTER TABLE public.properties OWNER TO postgres;

--
-- Name: properties_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.properties_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.properties_id_seq OWNER TO postgres;

--
-- Name: properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.properties_id_seq OWNED BY public.properties.id;


--
-- Name: property_amenities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.property_amenities (
    property_id bigint NOT NULL,
    amenity_id uuid NOT NULL
);


ALTER TABLE public.property_amenities OWNER TO postgres;

--
-- Name: property_highlights; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.property_highlights (
    id bigint NOT NULL,
    property_id bigint NOT NULL,
    title character varying(255),
    subtitle character varying(255),
    icon character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.property_highlights OWNER TO postgres;

--
-- Name: property_highlights_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.property_highlights_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.property_highlights_id_seq OWNER TO postgres;

--
-- Name: property_highlights_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.property_highlights_id_seq OWNED BY public.property_highlights.id;


--
-- Name: property_images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.property_images (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    property_id bigint NOT NULL,
    image_url text NOT NULL,
    alt_text character varying(255),
    title character varying(255),
    display_order integer DEFAULT 0,
    is_primary boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.property_images OWNER TO postgres;

--
-- Name: reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reports (
    report_id bigint NOT NULL,
    property_id bigint NOT NULL,
    user_id bigint NOT NULL,
    report_reason character varying(255) NOT NULL,
    report_status character varying(50) DEFAULT 'pending'::character varying,
    report_reply character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.reports OWNER TO postgres;

--
-- Name: reports_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reports_report_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reports_report_id_seq OWNER TO postgres;

--
-- Name: reports_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reports_report_id_seq OWNED BY public.reports.report_id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    booking_id uuid,
    reviewer_id bigint NOT NULL,
    reviewee_id bigint NOT NULL,
    property_id bigint NOT NULL,
    rating numeric(3,2) NOT NULL,
    review_text text,
    review_type character varying(50) NOT NULL,
    response_text text,
    is_visible boolean DEFAULT true,
    accuracy_rating numeric(3,2),
    checking_rating numeric(3,2),
    cleanliness_rating numeric(3,2),
    communication_rating numeric(3,2),
    location_rating numeric(3,2),
    value_rating numeric(3,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_rating CHECK (((rating >= (1)::numeric) AND (rating <= (5)::numeric)))
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- Name: second_chance_offers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.second_chance_offers (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    bid_id uuid NOT NULL,
    offered_check_in date NOT NULL,
    offered_check_out date NOT NULL,
    response_deadline timestamp without time zone NOT NULL,
    status public.offer_status DEFAULT 'WAITING'::public.offer_status,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    responded_at timestamp without time zone
);


ALTER TABLE public.second_chance_offers OWNER TO postgres;

--
-- Name: subscription; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscription (
    id bigint NOT NULL,
    endpoint character varying(255) NOT NULL,
    p256dh character varying(255) NOT NULL,
    auth character varying(255) NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.subscription OWNER TO postgres;

--
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscription_id_seq OWNER TO postgres;

--
-- Name: subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscription_id_seq OWNED BY public.subscription.id;


--
-- Name: systemlogs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.systemlogs (
    id bigint NOT NULL,
    type character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.systemlogs OWNER TO postgres;

--
-- Name: systemlogs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.systemlogs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.systemlogs_id_seq OWNER TO postgres;

--
-- Name: systemlogs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.systemlogs_id_seq OWNED BY public.systemlogs.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    email character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    password_hash character varying(255),
    full_name character varying(255) NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    profile_image_url text,
    verification_status character varying(50),
    is_active boolean DEFAULT true,
    is_admin boolean DEFAULT false,
    is_super_host boolean DEFAULT false,
    host_about text,
    host_review_count integer,
    host_rating_average numeric(3,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email_format CHECK (((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: wishlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wishlist (
    id integer NOT NULL,
    user_id integer NOT NULL,
    property_id integer NOT NULL,
    is_private boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.wishlist OWNER TO postgres;

--
-- Name: wishlist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.wishlist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wishlist_id_seq OWNER TO postgres;

--
-- Name: wishlist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.wishlist_id_seq OWNED BY public.wishlist.id;


--
-- Name: wishlist_property; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wishlist_property (
    wishlist_id bigint NOT NULL,
    property_id bigint NOT NULL,
    added_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE public.payment_sessions (
  id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
  user_id bigint NOT NULL,
  auction_id uuid NOT NULL,
  bid_id uuid NOT NULL,
  app_trans_id varchar(64) NOT NULL UNIQUE,
  amount numeric(10,2) NOT NULL,
  selected_nights jsonb NOT NULL,
  status varchar(50) NOT NULL DEFAULT 'INITIATED',
  idempotency_key varchar(128) UNIQUE,
  expires_at timestamp without time zone,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.payment_transactions (
  id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
  session_id uuid NOT NULL REFERENCES public.payment_sessions(id) ON DELETE CASCADE,
  app_trans_id varchar(64) NOT NULL,
  zp_trans_id varchar(64),
  amount numeric(10,2) NOT NULL,
  status varchar(50) NOT NULL DEFAULT 'PENDING',
  paid_at timestamp without time zone,
  raw jsonb,
  created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payment_transactions_app_trans_id ON public.payment_transactions (app_trans_id);

-- Optional: updated_at trigger like existing tables
CREATE TRIGGER trg_payment_sessions_upd BEFORE UPDATE ON public.payment_sessions
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
CREATE TRIGGER trg_payment_transactions_upd BEFORE UPDATE ON public.payment_transactions
FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


ALTER TABLE public.wishlist_property OWNER TO postgres;

--
-- Name: banners banner_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.banners ALTER COLUMN banner_id SET DEFAULT nextval('public.banners_banner_id_seq'::regclass);


--
-- Name: calendar_availability id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendar_availability ALTER COLUMN id SET DEFAULT nextval('public.calendar_availability_id_seq'::regclass);


--
-- Name: configuration id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuration ALTER COLUMN id SET DEFAULT nextval('public.configuration_id_seq'::regclass);


--
-- Name: conversation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversation ALTER COLUMN id SET DEFAULT nextval('public.conversation_id_seq'::regclass);


--
-- Name: house_rules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.house_rules ALTER COLUMN id SET DEFAULT nextval('public.house_rules_id_seq'::regclass);


--
-- Name: location_descriptions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_descriptions ALTER COLUMN id SET DEFAULT nextval('public.location_descriptions_id_seq'::regclass);


--
-- Name: message id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message ALTER COLUMN id SET DEFAULT nextval('public.message_id_seq'::regclass);


--
-- Name: notification id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification ALTER COLUMN id SET DEFAULT nextval('public.notification_id_seq'::regclass);


--
-- Name: properties id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.properties ALTER COLUMN id SET DEFAULT nextval('public.properties_id_seq'::regclass);


--
-- Name: property_highlights id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_highlights ALTER COLUMN id SET DEFAULT nextval('public.property_highlights_id_seq'::regclass);


--
-- Name: reports report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports ALTER COLUMN report_id SET DEFAULT nextval('public.reports_report_id_seq'::regclass);


--
-- Name: subscription id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription ALTER COLUMN id SET DEFAULT nextval('public.subscription_id_seq'::regclass);


--
-- Name: systemlogs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.systemlogs ALTER COLUMN id SET DEFAULT nextval('public.systemlogs_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: wishlist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist ALTER COLUMN id SET DEFAULT nextval('public.wishlist_id_seq'::regclass);


--
-- Name: amenities amenities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amenities
    ADD CONSTRAINT amenities_pkey PRIMARY KEY (id);


--
-- Name: auctions auctions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auctions
    ADD CONSTRAINT auctions_pkey PRIMARY KEY (id);


--
-- Name: banners banners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.banners
    ADD CONSTRAINT banners_pkey PRIMARY KEY (banner_id);


--
-- Name: bid_events bid_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bid_events
    ADD CONSTRAINT bid_events_pkey PRIMARY KEY (id);


--
-- Name: bid_notifications bid_notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bid_notifications
    ADD CONSTRAINT bid_notifications_pkey PRIMARY KEY (id);


--
-- Name: bids bids_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bids
    ADD CONSTRAINT bids_pkey PRIMARY KEY (id);


--
-- Name: bookings bookings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (id);


--
-- Name: calendar_availability calendar_availability_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendar_availability
    ADD CONSTRAINT calendar_availability_pkey PRIMARY KEY (id);


--
-- Name: calendar_availability calendar_availability_property_id_date_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendar_availability
    ADD CONSTRAINT calendar_availability_property_id_date_key UNIQUE (property_id, date);


--
-- Name: configuration configuration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuration
    ADD CONSTRAINT configuration_pkey PRIMARY KEY (id);


--
-- Name: conversation conversation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversation
    ADD CONSTRAINT conversation_pkey PRIMARY KEY (id);


--
-- Name: house_rules house_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.house_rules
    ADD CONSTRAINT house_rules_pkey PRIMARY KEY (id);


--
-- Name: location_descriptions location_descriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_descriptions
    ADD CONSTRAINT location_descriptions_pkey PRIMARY KEY (id);


--
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (id);


--
-- Name: properties properties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.properties
    ADD CONSTRAINT properties_pkey PRIMARY KEY (id);


--
-- Name: property_amenities property_amenities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_amenities
    ADD CONSTRAINT property_amenities_pkey PRIMARY KEY (property_id, amenity_id);


--
-- Name: property_highlights property_highlights_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_highlights
    ADD CONSTRAINT property_highlights_pkey PRIMARY KEY (id);


--
-- Name: property_images property_images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_images
    ADD CONSTRAINT property_images_pkey PRIMARY KEY (id);


--
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (report_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: second_chance_offers second_chance_offers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.second_chance_offers
    ADD CONSTRAINT second_chance_offers_pkey PRIMARY KEY (id);


--
-- Name: subscription subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT subscription_pkey PRIMARY KEY (id);


--
-- Name: systemlogs systemlogs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.systemlogs
    ADD CONSTRAINT systemlogs_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: wishlist wishlist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT wishlist_pkey PRIMARY KEY (id);


--
-- Name: wishlist_property wishlist_property_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_property
    ADD CONSTRAINT wishlist_property_pkey PRIMARY KEY (wishlist_id, property_id);


--
-- Name: idx_auctions_window; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_auctions_window ON public.auctions USING btree (start_date, end_date);


--
-- Name: idx_bids_date_range; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_bids_date_range ON public.bids USING btree (check_in, check_out);


--
-- Name: idx_calendar_prop_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_calendar_prop_date ON public.calendar_availability USING btree (property_id, date);


--
-- Name: idx_properties_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_properties_location ON public.properties USING btree (city, state, country);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_email ON public.users USING btree (email);


--
-- Name: auctions trg_auctions_upd; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_auctions_upd BEFORE UPDATE ON public.auctions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: bookings trg_bookings_upd; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_bookings_upd BEFORE UPDATE ON public.bookings FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: properties trg_props_upd; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_props_upd BEFORE UPDATE ON public.properties FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: reviews trg_reviews_upd; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_reviews_upd BEFORE UPDATE ON public.reviews FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: users trg_users_upd; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_users_upd BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: auctions auctions_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auctions
    ADD CONSTRAINT auctions_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: auctions auctions_winner_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auctions
    ADD CONSTRAINT auctions_winner_user_id_fkey FOREIGN KEY (winner_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: bids bids_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bids
    ADD CONSTRAINT bids_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id) ON DELETE CASCADE;


--
-- Name: bids bids_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bids
    ADD CONSTRAINT bids_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: bookings bookings_auction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_auction_id_fkey FOREIGN KEY (auction_id) REFERENCES public.auctions(id) ON DELETE SET NULL;


--
-- Name: bookings bookings_guest_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_guest_id_fkey FOREIGN KEY (guest_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: bookings bookings_host_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_host_id_fkey FOREIGN KEY (host_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: bookings bookings_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: calendar_availability calendar_availability_bid_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendar_availability
    ADD CONSTRAINT calendar_availability_bid_id_fkey FOREIGN KEY (bid_id) REFERENCES public.bids(id) ON DELETE SET NULL;


--
-- Name: calendar_availability calendar_availability_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calendar_availability
    ADD CONSTRAINT calendar_availability_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: house_rules house_rules_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.house_rules
    ADD CONSTRAINT house_rules_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: location_descriptions location_descriptions_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_descriptions
    ADD CONSTRAINT location_descriptions_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: message message_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.conversation(id) ON DELETE CASCADE;


--
-- Name: properties properties_host_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.properties
    ADD CONSTRAINT properties_host_id_fkey FOREIGN KEY (host_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: property_amenities property_amenities_amenity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_amenities
    ADD CONSTRAINT property_amenities_amenity_id_fkey FOREIGN KEY (amenity_id) REFERENCES public.amenities(id) ON DELETE CASCADE;


--
-- Name: property_amenities property_amenities_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_amenities
    ADD CONSTRAINT property_amenities_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: property_highlights property_highlights_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_highlights
    ADD CONSTRAINT property_highlights_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: property_images property_images_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_images
    ADD CONSTRAINT property_images_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_booking_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.bookings(id) ON DELETE SET NULL;


--
-- Name: reviews reviews_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_reviewee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_reviewee_id_fkey FOREIGN KEY (reviewee_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_reviewer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: wishlist wishlist_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT wishlist_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.properties(id) ON DELETE CASCADE;


--
-- Name: wishlist wishlist_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist
    ADD CONSTRAINT wishlist_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

