-- Payment tables migration script (Corrected)
-- Changes:
-- - Uses numeric(10,2) for money amounts instead of integer
-- - Uses 'INITIATED' as default status to match production
-- - Includes order_url column
-- - Adds all necessary indexes

-- Create payment_sessions table
CREATE TABLE IF NOT EXISTS public.payment_sessions (
  id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
  user_id bigint NOT NULL,
  auction_id uuid NOT NULL,
  bid_id uuid NOT NULL,
  app_trans_id varchar(64) NOT NULL UNIQUE,
  amount numeric(10,2) NOT NULL,
  selected_nights jsonb NOT NULL,
  status varchar(50) NOT NULL DEFAULT 'INITIATED',
  idempotency_key varchar(128) UNIQUE,
  expires_at timestamp WITHOUT TIME ZONE,
  order_url text,
  created_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create payment_transactions table
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

-- Add foreign key constraints
ALTER TABLE IF EXISTS public.payment_sessions
  ADD CONSTRAINT fk_payment_sessions_auction_id FOREIGN KEY (auction_id)
  REFERENCES public.auctions(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.payment_sessions
  ADD CONSTRAINT fk_payment_sessions_bid_id FOREIGN KEY (bid_id)
  REFERENCES public.bids(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.payment_sessions
  ADD CONSTRAINT fk_payment_sessions_user_id FOREIGN KEY (user_id)
  REFERENCES public.users(id) ON DELETE CASCADE;

-- Create basic indexes (non-CONCURRENT for initial table creation)
CREATE INDEX IF NOT EXISTS idx_payment_sessions_app_trans_id ON public.payment_sessions(app_trans_id);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_app_trans_id ON public.payment_transactions(app_trans_id);

-- Create update triggers
DO $$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname = 'trg_payment_sessions_upd'
  ) THEN
    CREATE TRIGGER trg_payment_sessions_upd 
    BEFORE UPDATE ON public.payment_sessions 
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname = 'trg_payment_transactions_upd'
  ) THEN
    CREATE TRIGGER trg_payment_transactions_upd 
    BEFORE UPDATE ON public.payment_transactions 
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
  END IF;
END $$; 