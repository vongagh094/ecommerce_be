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
)

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