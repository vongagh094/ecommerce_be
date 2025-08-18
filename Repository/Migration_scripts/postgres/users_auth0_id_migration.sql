-- Users Auth0 ID Migration (Low Risk)
-- Purpose: Add nullable auth0_id column and a unique partial index for non-null values
-- Notes:
-- - CREATE INDEX CONCURRENTLY cannot run inside a transaction
-- - Adding a nullable column is metadata-only and fast

-- 1) Add column if it doesn't exist (guarded with DO block)
DO $$
BEGIN
	IF NOT EXISTS (
		SELECT 1 FROM information_schema.columns
		WHERE table_schema = 'public'
		  AND table_name = 'users'
		  AND column_name = 'auth0_id'
	) THEN
		ALTER TABLE public.users ADD COLUMN auth0_id varchar(255);
	END IF;
END$$;

-- 2) Create a unique partial index on auth0_id for non-null values
CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS users_auth0_id_unique_idx
ON public.users(auth0_id)
WHERE auth0_id IS NOT NULL; 