-- File: insert_properties.sql
-- Insert sample property types and categories if not exist
INSERT INTO public.property_types (name, description)
VALUES 
('Apartment', 'Urban living spaces'),
('House', 'Standalone homes'),
('Villa', 'Luxury residences'),
('Cabin', 'Rustic retreats'),
('Condo', 'Condominium units')
ON CONFLICT (name) DO NOTHING;

INSERT INTO public.property_categories (name, description)
VALUES 
('City', 'Urban properties'),
('Beach', 'Coastal locations'),
('Mountain', 'Highland retreats'),
('Rural', 'Countryside homes'),
('Luxury', 'High-end accommodations')
ON CONFLICT (name) DO NOTHING;

-- Insert 5 sample properties for host_id = 2884
INSERT INTO public.properties (
    host_id, title, description, property_type, category, max_guests, bedrooms, bathrooms,
    address_line1, city, state, country, postal_code, latitude, longitude,
    base_price, cleaning_fee, cancellation_policy, instant_book, minimum_stay,
    home_tier, is_guest_favorite, language, status
) VALUES 
(2884, 'Cozy City Apartment', 'A comfortable apartment in the heart of the city.', 'Apartment', 'City', 4, 2, 1, 
 '123 Main St', 'New York', 'NY', 'USA', '10001', 40.7128, -74.0060, 
 150.00, 20.00, 'Flexible', true, 1, 1, true, 'en', 'ACTIVE'),
 
(2884, 'Beachfront Villa', 'Luxury villa with ocean views.', 'Villa', 'Beach', 8, 4, 3, 
 '456 Ocean Ave', 'Miami', 'FL', 'USA', '33139', 25.7617, -80.1918, 
 500.00, 50.00, 'Strict', false, 3, 2, false, 'en', 'ACTIVE'),
 
(2884, 'Mountain Cabin Retreat', 'Rustic cabin in the mountains.', 'Cabin', 'Mountain', 6, 3, 2, 
 '789 Hill Rd', 'Denver', 'CO', 'USA', '80202', 39.7392, -104.9903, 
 200.00, 30.00, 'Moderate', true, 2, 1, true, 'en', 'ACTIVE'),
 
(2884, 'Rural Farmhouse', 'Charming farmhouse in the countryside.', 'House', 'Rural', 10, 5, 4, 
 '101 Farm Ln', 'Austin', 'TX', 'USA', '78701', 30.2672, -97.7431, 
 300.00, 40.00, 'Flexible', false, 1, 3, false, 'en', 'ACTIVE'),
 
(2884, 'Luxury Condo Downtown', 'High-end condo with city skyline views.', 'Condo', 'Luxury', 5, 2, 2, 
 '202 Skyline Blvd', 'Chicago', 'IL', 'USA', '60601', 41.8781, -87.6298, 
 400.00, 45.00, 'Strict', true, 2, 2, true, 'en', 'ACTIVE');

-- File: insert_auctions.sql
-- Insert 18 auctions per property: 12 for 2024 (one per month), 6 for 2025 (Jan, Mar, May, Jul, Sep, Nov)
-- For host_id=2884, properties 1 to 5

-- Auctions for Property 1 (Cozy City Apartment)
INSERT INTO public.auctions (
    id, property_id, start_date, end_date, min_nights, max_nights, starting_price, minimum_bid, bid_increment,
    auction_start_time, auction_end_time, objective, status
) VALUES 
(uuid_generate_v4(), 1, '2024-01-01', '2024-01-31', 1, 7, 100.00, 120.00, 10.00, '2024-01-01 00:00:00', '2024-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-02-01', '2024-02-29', 1, 7, 95.00, 115.00, 10.00, '2024-02-01 00:00:00', '2024-02-29 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-03-01', '2024-03-31', 1, 7, 110.00, 130.00, 12.00, '2024-03-01 00:00:00', '2024-03-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-04-01', '2024-04-30', 1, 7, 120.00, 140.00, 12.00, '2024-04-01 00:00:00', '2024-04-30 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-05-01', '2024-05-31', 1, 7, 130.00, 150.00, 15.00, '2024-05-01 00:00:00', '2024-05-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-06-01', '2024-06-30', 2, 10, 150.00, 170.00, 15.00, '2024-06-01 00:00:00', '2024-06-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-07-01', '2024-07-31', 2, 10, 160.00, 180.00, 15.00, '2024-07-01 00:00:00', '2024-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-08-01', '2024-08-31', 2, 10, 155.00, 175.00, 15.00, '2024-08-01 00:00:00', '2024-08-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-09-01', '2024-09-30', 1, 7, 140.00, 160.00, 12.00, '2024-09-01 00:00:00', '2024-09-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-10-01', '2024-10-31', 1, 7, 135.00, 155.00, 12.00, '2024-10-01 00:00:00', '2024-10-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-11-01', '2024-11-30', 1, 7, 145.00, 165.00, 15.00, '2024-11-01 00:00:00', '2024-11-30 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 1, '2024-12-01', '2024-12-31', 1, 7, 170.00, 190.00, 20.00, '2024-12-01 00:00:00', '2024-12-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 1, '2025-01-01', '2025-01-31', 1, 7, 180.00, 200.00, 20.00, '2025-01-01 00:00:00', '2025-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 1, '2025-03-01', '2025-03-31', 1, 7, 190.00, 210.00, 20.00, '2025-03-01 00:00:00', '2025-03-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 1, '2025-05-01', '2025-05-31', 1, 7, 200.00, 220.00, 22.00, '2025-05-01 00:00:00', '2025-05-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 1, '2025-07-01', '2025-07-31', 2, 10, 210.00, 230.00, 25.00, '2025-07-01 00:00:00', '2025-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 1, '2025-09-01', '2025-09-30', 1, 7, 195.00, 215.00, 20.00, '2025-09-01 00:00:00', '2025-09-30 23:59:59', 'HIGHEST_PER_NIGHT', 'PENDING'),
(uuid_generate_v4(), 1, '2025-11-01', '2025-11-30', 1, 7, 205.00, 225.00, 22.00, '2025-11-01 00:00:00', '2025-11-30 23:59:59', 'HYBRID', 'PENDING');

-- Auctions for Property 2 (Beachfront Villa)
INSERT INTO public.auctions (
    id, property_id, start_date, end_date, min_nights, max_nights, starting_price, minimum_bid, bid_increment,
    auction_start_time, auction_end_time, objective, status
) VALUES 
(uuid_generate_v4(), 2, '2024-01-01', '2024-01-31', 3, 14, 400.00, 450.00, 50.00, '2024-01-01 00:00:00', '2024-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-02-01', '2024-02-29', 3, 14, 380.00, 430.00, 45.00, '2024-02-01 00:00:00', '2024-02-29 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-03-01', '2024-03-31', 3, 14, 420.00, 470.00, 50.00, '2024-03-01 00:00:00', '2024-03-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-04-01', '2024-04-30', 3, 14, 450.00, 500.00, 55.00, '2024-04-01 00:00:00', '2024-04-30 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-05-01', '2024-05-31', 3, 14, 500.00, 550.00, 60.00, '2024-05-01 00:00:00', '2024-05-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-06-01', '2024-06-30', 4, 15, 550.00, 600.00, 65.00, '2024-06-01 00:00:00', '2024-06-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-07-01', '2024-07-31', 4, 15, 600.00, 650.00, 70.00, '2024-07-01 00:00:00', '2024-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-08-01', '2024-08-31', 4, 15, 580.00, 630.00, 65.00, '2024-08-01 00:00:00', '2024-08-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-09-01', '2024-09-30', 3, 14, 520.00, 570.00, 60.00, '2024-09-01 00:00:00', '2024-09-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-10-01', '2024-10-31', 3, 14, 500.00, 550.00, 55.00, '2024-10-01 00:00:00', '2024-10-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-11-01', '2024-11-30', 3, 14, 530.00, 580.00, 60.00, '2024-11-01 00:00:00', '2024-11-30 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 2, '2024-12-01', '2024-12-31', 3, 14, 600.00, 650.00, 70.00, '2024-12-01 00:00:00', '2024-12-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 2, '2025-01-01', '2025-01-31', 3, 14, 620.00, 670.00, 70.00, '2025-01-01 00:00:00', '2025-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 2, '2025-03-01', '2025-03-31', 3, 14, 640.00, 690.00, 75.00, '2025-03-01 00:00:00', '2025-03-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 2, '2025-05-01', '2025-05-31', 3, 14, 660.00, 710.00, 75.00, '2025-05-01 00:00:00', '2025-05-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 2, '2025-07-01', '2025-07-31', 4, 15, 680.00, 730.00, 80.00, '2025-07-01 00:00:00', '2025-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 2, '2025-09-01', '2025-09-30', 3, 14, 650.00, 700.00, 75.00, '2025-09-01 00:00:00', '2025-09-30 23:59:59', 'HIGHEST_PER_NIGHT', 'PENDING'),
(uuid_generate_v4(), 2, '2025-11-01', '2025-11-30', 3, 14, 670.00, 720.00, 80.00, '2025-11-01 00:00:00', '2025-11-30 23:59:59', 'HYBRID', 'PENDING');

-- Auctions for Property 3 (Mountain Cabin Retreat)
INSERT INTO public.auctions (
    id, property_id, start_date, end_date, min_nights, max_nights, starting_price, minimum_bid, bid_increment,
    auction_start_time, auction_end_time, objective, status
) VALUES 
(uuid_generate_v4(), 3, '2024-01-01', '2024-01-31', 1, 7, 150.00, 170.00, 15.00, '2024-01-01 00:00:00', '2024-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-02-01', '2024-02-29', 1, 7, 140.00, 160.00, 15.00, '2024-02-01 00:00:00', '2024-02-29 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-03-01', '2024-03-31', 1, 7, 160.00, 180.00, 18.00, '2024-03-01 00:00:00', '2024-03-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-04-01', '2024-04-30', 1, 7, 170.00, 190.00, 18.00, '2024-04-01 00:00:00', '2024-04-30 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-05-01', '2024-05-31', 1, 7, 180.00, 200.00, 20.00, '2024-05-01 00:00:00', '2024-05-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-06-01', '2024-06-30', 2, 8, 200.00, 220.00, 22.00, '2024-06-01 00:00:00', '2024-06-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-07-01', '2024-07-31', 2, 8, 210.00, 230.00, 22.00, '2024-07-01 00:00:00', '2024-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-08-01', '2024-08-31', 2, 8, 205.00, 225.00, 22.00, '2024-08-01 00:00:00', '2024-08-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-09-01', '2024-09-30', 1, 7, 190.00, 210.00, 20.00, '2024-09-01 00:00:00', '2024-09-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-10-01', '2024-10-31', 1, 7, 185.00, 205.00, 20.00, '2024-10-01 00:00:00', '2024-10-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-11-01', '2024-11-30', 1, 7, 195.00, 215.00, 20.00, '2024-11-01 00:00:00', '2024-11-30 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 3, '2024-12-01', '2024-12-31', 1, 7, 220.00, 240.00, 25.00, '2024-12-01 00:00:00', '2024-12-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 3, '2025-01-01', '2025-01-31', 1, 7, 230.00, 250.00, 25.00, '2025-01-01 00:00:00', '2025-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 3, '2025-03-01', '2025-03-31', 1, 7, 240.00, 260.00, 25.00, '2025-03-01 00:00:00', '2025-03-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 3, '2025-05-01', '2025-05-31', 1, 7, 250.00, 270.00, 27.00, '2025-05-01 00:00:00', '2025-05-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 3, '2025-07-01', '2025-07-31', 2, 8, 260.00, 280.00, 28.00, '2025-07-01 00:00:00', '2025-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 3, '2025-09-01', '2025-09-30', 1, 7, 245.00, 265.00, 25.00, '2025-09-01 00:00:00', '2025-09-30 23:59:59', 'HIGHEST_PER_NIGHT', 'PENDING'),
(uuid_generate_v4(), 3, '2025-11-01', '2025-11-30', 1, 7, 255.00, 275.00, 27.00, '2025-11-01 00:00:00', '2025-11-30 23:59:59', 'HYBRID', 'PENDING');

-- Auctions for Property 4 (Rural Farmhouse)
INSERT INTO public.auctions (
    id, property_id, start_date, end_date, min_nights, max_nights, starting_price, minimum_bid, bid_increment,
    auction_start_time, auction_end_time, objective, status
) VALUES 
(uuid_generate_v4(), 4, '2024-01-01', '2024-01-31', 2, 10, 250.00, 280.00, 25.00, '2024-01-01 00:00:00', '2024-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-02-01', '2024-02-29', 2, 10, 240.00, 270.00, 25.00, '2024-02-01 00:00:00', '2024-02-29 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-03-01', '2024-03-31', 2, 10, 260.00, 290.00, 28.00, '2024-03-01 00:00:00', '2024-03-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-04-01', '2024-04-30', 2, 10, 270.00, 300.00, 30.00, '2024-04-01 00:00:00', '2024-04-30 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-05-01', '2024-05-31', 2, 10, 280.00, 310.00, 30.00, '2024-05-01 00:00:00', '2024-05-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-06-01', '2024-06-30', 3, 12, 300.00, 330.00, 33.00, '2024-06-01 00:00:00', '2024-06-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-07-01', '2024-07-31', 3, 12, 310.00, 340.00, 34.00, '2024-07-01 00:00:00', '2024-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-08-01', '2024-08-31', 3, 12, 305.00, 335.00, 33.00, '2024-08-01 00:00:00', '2024-08-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-09-01', '2024-09-30', 2, 10, 290.00, 320.00, 30.00, '2024-09-01 00:00:00', '2024-09-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-10-01', '2024-10-31', 2, 10, 285.00, 315.00, 30.00, '2024-10-01 00:00:00', '2024-10-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-11-01', '2024-11-30', 2, 10, 295.00, 325.00, 32.00, '2024-11-01 00:00:00', '2024-11-30 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 4, '2024-12-01', '2024-12-31', 2, 10, 320.00, 350.00, 35.00, '2024-12-01 00:00:00', '2024-12-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 4, '2025-01-01', '2025-01-31', 2, 10, 330.00, 360.00, 36.00, '2025-01-01 00:00:00', '2025-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 4, '2025-03-01', '2025-03-31', 2, 10, 340.00, 370.00, 37.00, '2025-03-01 00:00:00', '2025-03-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 4, '2025-05-01', '2025-05-31', 2, 10, 350.00, 380.00, 38.00, '2025-05-01 00:00:00', '2025-05-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 4, '2025-07-01', '2025-07-31', 3, 12, 360.00, 390.00, 39.00, '2025-07-01 00:00:00', '2025-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 4, '2025-09-01', '2025-09-30', 2, 10, 345.00, 375.00, 37.00, '2025-09-01 00:00:00', '2025-09-30 23:59:59', 'HIGHEST_PER_NIGHT', 'PENDING'),
(uuid_generate_v4(), 4, '2025-11-01', '2025-11-30', 2, 10, 355.00, 385.00, 38.00, '2025-11-01 00:00:00', '2025-11-30 23:59:59', 'HYBRID', 'PENDING');

-- Auctions for Property 5 (Luxury Condo Downtown)
INSERT INTO public.auctions (
    id, property_id, start_date, end_date, min_nights, max_nights, starting_price, minimum_bid, bid_increment,
    auction_start_time, auction_end_time, objective, status
) VALUES 
(uuid_generate_v4(), 5, '2024-01-01', '2024-01-31', 1, 5, 300.00, 320.00, 30.00, '2024-01-01 00:00:00', '2024-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-02-01', '2024-02-29', 1, 5, 290.00, 310.00, 30.00, '2024-02-01 00:00:00', '2024-02-29 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-03-01', '2024-03-31', 1, 5, 310.00, 330.00, 33.00, '2024-03-01 00:00:00', '2024-03-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-04-01', '2024-04-30', 1, 5, 320.00, 340.00, 34.00, '2024-04-01 00:00:00', '2024-04-30 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-05-01', '2024-05-31', 1, 5, 330.00, 350.00, 35.00, '2024-05-01 00:00:00', '2024-05-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-06-01', '2024-06-30', 2, 7, 350.00, 370.00, 37.00, '2024-06-01 00:00:00', '2024-06-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-07-01', '2024-07-31', 2, 7, 360.00, 380.00, 38.00, '2024-07-01 00:00:00', '2024-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-08-01', '2024-08-31', 2, 7, 355.00, 375.00, 37.00, '2024-08-01 00:00:00', '2024-08-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-09-01', '2024-09-30', 1, 5, 340.00, 360.00, 36.00, '2024-09-01 00:00:00', '2024-09-30 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-10-01', '2024-10-31', 1, 5, 335.00, 355.00, 35.00, '2024-10-01 00:00:00', '2024-10-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-11-01', '2024-11-30', 1, 5, 345.00, 365.00, 36.00, '2024-11-01 00:00:00', '2024-11-30 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 5, '2024-12-01', '2024-12-31', 1, 5, 370.00, 390.00, 39.00, '2024-12-01 00:00:00', '2024-12-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 5, '2025-01-01', '2025-01-31', 1, 5, 380.00, 400.00, 40.00, '2025-01-01 00:00:00', '2025-01-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 5, '2025-03-01', '2025-03-31', 1, 5, 390.00, 410.00, 41.00, '2025-03-01 00:00:00', '2025-03-31 23:59:59', 'HIGHEST_PER_NIGHT', 'COMPLETED'),
(uuid_generate_v4(), 5, '2025-05-01', '2025-05-31', 1, 5, 400.00, 420.00, 42.00, '2025-05-01 00:00:00', '2025-05-31 23:59:59', 'HYBRID', 'COMPLETED'),
(uuid_generate_v4(), 5, '2025-07-01', '2025-07-31', 2, 7, 410.00, 430.00, 43.00, '2025-07-01 00:00:00', '2025-07-31 23:59:59', 'HIGHEST_TOTAL', 'COMPLETED'),
(uuid_generate_v4(), 5, '2025-09-01', '2025-09-30', 1, 5, 395.00, 415.00, 41.00, '2025-09-01 00:00:00', '2025-09-30 23:59:59', 'HIGHEST_PER_NIGHT', 'PENDING'),
(uuid_generate_v4(), 5, '2025-11-01', '2025-11-30', 1, 5, 405.00, 425.00, 42.00, '2025-11-01 00:00:00', '2025-11-30 23:59:59', 'HYBRID', 'PENDING');

-- File: insert_bookings.sql
-- Insert one booking per auction, with check_in_date and check_out_date within auction's start_date and end_date
-- Define CTEs within each INSERT to ensure scope for guest_id cycling
-- Select valid guest_id values from users table, excluding host_id=2884
-- Covers all months in 2024 and 6 months in 2025 (Jan, Mar, May, Jul, Sep, Nov) for each property
-- Host_id=2884, varied total_nights, base_amount, cleaning_fee, taxes for dashboard stats

-- Bookings for Property 1 (Cozy City Apartment)
WITH valid_guests AS (
    SELECT id
    FROM public.users
    WHERE id != 2884  -- Exclude host_id
    LIMIT 10
),
cycled_guests AS (
    SELECT id, ROW_NUMBER() OVER () - 1 AS row_num
    FROM valid_guests
),
guest_cycle AS (
    SELECT id, row_num
    FROM cycled_guests
)
INSERT INTO public.bookings (
    id, auction_id, property_id, guest_id, host_id, check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount, booking_status, payment_status
) VALUES 
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-01-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2024-01-10', '2024-01-15', 5, 500.00, 20.00, 50.00, 570.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-02-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2024-02-05', '2024-02-10', 5, 480.00, 20.00, 48.00, 548.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-03-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2024-03-10', '2024-03-15', 5, 520.00, 20.00, 52.00, 592.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-04-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2024-04-05', '2024-04-10', 5, 540.00, 20.00, 54.00, 614.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-05-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2024-05-10', '2024-05-15', 5, 560.00, 20.00, 56.00, 636.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-06-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2024-06-05', '2024-06-12', 7, 700.00, 20.00, 70.00, 790.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-07-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2024-07-10', '2024-07-17', 7, 720.00, 20.00, 72.00, 812.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-08-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2024-08-05', '2024-08-12', 7, 710.00, 20.00, 71.00, 801.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-09-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2024-09-10', '2024-09-15', 5, 580.00, 20.00, 58.00, 658.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-10-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2024-10-05', '2024-10-10', 5, 570.00, 20.00, 57.00, 647.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-11-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2024-11-10', '2024-11-15', 5, 600.00, 20.00, 60.00, 680.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2024-12-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2024-12-05', '2024-12-12', 7, 740.00, 20.00, 74.00, 834.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2025-01-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2025-01-10', '2025-01-15', 5, 760.00, 20.00, 76.00, 856.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2025-03-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2025-03-05', '2025-03-10', 5, 780.00, 20.00, 78.00, 878.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2025-05-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2025-05-10', '2025-05-15', 5, 800.00, 20.00, 80.00, 900.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2025-07-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2025-07-05', '2025-07-12', 7, 820.00, 20.00, 82.00, 922.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2025-09-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2025-09-10', '2025-09-15', 5, 790.00, 20.00, 79.00, 889.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=1 AND start_date='2025-11-01'), 1, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2025-11-05', '2025-11-12', 7, 830.00, 20.00, 83.00, 933.00, 'CONFIRMED', 'PAID');

-- Bookings for Property 2 (Beachfront Villa)
WITH valid_guests AS (
    SELECT id
    FROM public.users
    WHERE id != 2884
    LIMIT 10
),
cycled_guests AS (
    SELECT id, ROW_NUMBER() OVER () - 1 AS row_num
    FROM valid_guests
),
guest_cycle AS (
    SELECT id, row_num
    FROM cycled_guests
)
INSERT INTO public.bookings (
    id, auction_id, property_id, guest_id, host_id, check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount, booking_status, payment_status
) VALUES 
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-01-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2024-01-10', '2024-01-17', 7, 2000.00, 50.00, 200.00, 2250.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-02-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2024-02-05', '2024-02-12', 7, 1900.00, 50.00, 190.00, 2140.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-03-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2024-03-10', '2024-03-17', 7, 2100.00, 50.00, 210.00, 2360.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-04-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2024-04-05', '2024-04-12', 7, 2200.00, 50.00, 220.00, 2470.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-05-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2024-05-10', '2024-05-17', 7, 2300.00, 50.00, 230.00, 2580.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-06-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2024-06-05', '2024-06-13', 8, 2500.00, 50.00, 250.00, 2800.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-07-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2024-07-10', '2024-07-18', 8, 2600.00, 50.00, 260.00, 2910.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-08-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2024-08-05', '2024-08-13', 8, 2550.00, 50.00, 255.00, 2855.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-09-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2024-09-10', '2024-09-17', 7, 2400.00, 50.00, 240.00, 2690.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-10-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2024-10-05', '2024-10-12', 7, 2350.00, 50.00, 235.00, 2635.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-11-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2024-11-10', '2024-11-17', 7, 2450.00, 50.00, 245.00, 2745.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2024-12-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2024-12-05', '2024-12-13', 8, 2700.00, 50.00, 270.00, 3020.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2025-01-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2025-01-10', '2025-01-17', 7, 2800.00, 50.00, 280.00, 3130.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2025-03-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2025-03-05', '2025-03-13', 8, 2900.00, 50.00, 290.00, 3240.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2025-05-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2025-05-10', '2025-05-17', 7, 3000.00, 50.00, 300.00, 3350.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2025-07-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2025-07-05', '2025-07-13', 8, 3100.00, 50.00, 310.00, 3460.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2025-09-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2025-09-10', '2025-09-17', 7, 2950.00, 50.00, 295.00, 3295.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=2 AND start_date='2025-11-01'), 2, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2025-11-05', '2025-11-13', 8, 3050.00, 50.00, 305.00, 3405.00, 'CONFIRMED', 'PAID');

-- Bookings for Property 3 (Mountain Cabin Retreat)
WITH valid_guests AS (
    SELECT id
    FROM public.users
    WHERE id != 2884
    LIMIT 10
),
cycled_guests AS (
    SELECT id, ROW_NUMBER() OVER () - 1 AS row_num
    FROM valid_guests
),
guest_cycle AS (
    SELECT id, row_num
    FROM cycled_guests
)
INSERT INTO public.bookings (
    id, auction_id, property_id, guest_id, host_id, check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount, booking_status, payment_status
) VALUES 
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-01-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2024-01-10', '2024-01-15', 5, 900.00, 30.00, 90.00, 1020.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-02-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2024-02-05', '2024-02-10', 5, 880.00, 30.00, 88.00, 998.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-03-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2024-03-10', '2024-03-15', 5, 920.00, 30.00, 92.00, 1042.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-04-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2024-04-05', '2024-04-10', 5, 940.00, 30.00, 94.00, 1064.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-05-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2024-05-10', '2024-05-15', 5, 960.00, 30.00, 96.00, 1086.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-06-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2024-06-05', '2024-06-12', 7, 1000.00, 30.00, 100.00, 1130.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-07-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2024-07-10', '2024-07-17', 7, 1020.00, 30.00, 102.00, 1152.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-08-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2024-08-05', '2024-08-12', 7, 1010.00, 30.00, 101.00, 1141.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-09-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2024-09-10', '2024-09-15', 5, 980.00, 30.00, 98.00, 1108.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-10-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2024-10-05', '2024-10-10', 5, 970.00, 30.00, 97.00, 1097.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-11-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2024-11-10', '2024-11-15', 5, 990.00, 30.00, 99.00, 1119.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2024-12-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2024-12-05', '2024-12-12', 7, 1050.00, 30.00, 105.00, 1185.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2025-01-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2025-01-10', '2025-01-15', 5, 1070.00, 30.00, 107.00, 1207.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2025-03-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2025-03-05', '2025-03-10', 5, 1090.00, 30.00, 109.00, 1229.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2025-05-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2025-05-10', '2025-05-15', 5, 1110.00, 30.00, 111.00, 1251.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2025-07-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2025-07-05', '2025-07-12', 7, 1130.00, 30.00, 113.00, 1273.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2025-09-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2025-09-10', '2025-09-15', 5, 1100.00, 30.00, 110.00, 1240.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=3 AND start_date='2025-11-01'), 3, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2025-11-05', '2025-11-12', 7, 1140.00, 30.00, 114.00, 1284.00, 'CONFIRMED', 'PAID');

-- Bookings for Property 4 (Rural Farmhouse)
WITH valid_guests AS (
    SELECT id
    FROM public.users
    WHERE id != 2884
    LIMIT 10
),
cycled_guests AS (
    SELECT id, ROW_NUMBER() OVER () - 1 AS row_num
    FROM valid_guests
),
guest_cycle AS (
    SELECT id, row_num
    FROM cycled_guests
)
INSERT INTO public.bookings (
    id, auction_id, property_id, guest_id, host_id, check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount, booking_status, payment_status
) VALUES 
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-01-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2024-01-10', '2024-01-17', 7, 1400.00, 40.00, 140.00, 1580.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-02-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2024-02-05', '2024-02-12', 7, 1350.00, 40.00, 135.00, 1525.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-03-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2024-03-10', '2024-03-17', 7, 1450.00, 40.00, 145.00, 1635.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-04-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2024-04-05', '2024-04-12', 7, 1500.00, 40.00, 150.00, 1690.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-05-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2024-05-10', '2024-05-17', 7, 1550.00, 40.00, 155.00, 1745.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-06-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2024-06-05', '2024-06-13', 8, 1600.00, 40.00, 160.00, 1800.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-07-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2024-07-10', '2024-07-18', 8, 1650.00, 40.00, 165.00, 1855.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-08-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2024-08-05', '2024-08-13', 8, 1625.00, 40.00, 162.50, 1827.50, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-09-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2024-09-10', '2024-09-17', 7, 1575.00, 40.00, 157.50, 1772.50, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-10-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2024-10-05', '2024-10-12', 7, 1550.00, 40.00, 155.00, 1745.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-11-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2024-11-10', '2024-11-17', 7, 1600.00, 40.00, 160.00, 1800.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2024-12-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2024-12-05', '2024-12-13', 8, 1700.00, 40.00, 170.00, 1910.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2025-01-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2025-01-10', '2025-01-17', 7, 1750.00, 40.00, 175.00, 1965.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2025-03-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2025-03-05', '2025-03-13', 8, 1800.00, 40.00, 180.00, 2020.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2025-05-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2025-05-10', '2025-05-17', 7, 1850.00, 40.00, 185.00, 2075.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2025-07-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2025-07-05', '2025-07-13', 8, 1900.00, 40.00, 190.00, 2130.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2025-09-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2025-09-10', '2025-09-17', 7, 1825.00, 40.00, 182.50, 2047.50, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=4 AND start_date='2025-11-01'), 4, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2025-11-05', '2025-11-13', 8, 1875.00, 40.00, 187.50, 2102.50, 'CONFIRMED', 'PAID');

-- Bookings for Property 5 (Luxury Condo Downtown)
WITH valid_guests AS (
    SELECT id
    FROM public.users
    WHERE id != 2884
    LIMIT 10
),
cycled_guests AS (
    SELECT id, ROW_NUMBER() OVER () - 1 AS row_num
    FROM valid_guests
),
guest_cycle AS (
    SELECT id, row_num
    FROM cycled_guests
)
INSERT INTO public.bookings (
    id, auction_id, property_id, guest_id, host_id, check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount, booking_status, payment_status
) VALUES 
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-01-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2024-01-10', '2024-01-15', 5, 1200.00, 45.00, 120.00, 1365.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-02-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2024-02-05', '2024-02-10', 5, 1150.00, 45.00, 115.00, 1310.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-03-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2024-03-10', '2024-03-15', 5, 1250.00, 45.00, 125.00, 1420.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-04-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2024-04-05', '2024-04-10', 5, 1300.00, 45.00, 130.00, 1475.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-05-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2024-05-10', '2024-05-15', 5, 1350.00, 45.00, 135.00, 1530.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-06-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2024-06-05', '2024-06-12', 7, 1400.00, 45.00, 140.00, 1585.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-07-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2024-07-10', '2024-07-17', 7, 1450.00, 45.00, 145.00, 1640.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-08-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2024-08-05', '2024-08-12', 7, 1425.00, 45.00, 142.50, 1612.50, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-09-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 0), 2884, '2024-09-10', '2024-09-15', 5, 1375.00, 45.00, 137.50, 1557.50, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-10-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 1), 2884, '2024-10-05', '2024-10-10', 5, 1350.00, 45.00, 135.00, 1530.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-11-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 2), 2884, '2024-11-10', '2024-11-15', 5, 1400.00, 45.00, 140.00, 1585.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2024-12-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 3), 2884, '2024-12-05', '2024-12-12', 7, 1500.00, 45.00, 150.00, 1695.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2025-01-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 4), 2884, '2025-01-10', '2025-01-15', 5, 1550.00, 45.00, 155.00, 1750.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2025-03-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 5), 2884, '2025-03-05', '2025-03-10', 5, 1600.00, 45.00, 160.00, 1805.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2025-05-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 6), 2884, '2025-05-10', '2025-05-15', 5, 1650.00, 45.00, 165.00, 1860.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2025-07-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 7), 2884, '2025-07-05', '2025-07-12', 7, 1700.00, 45.00, 170.00, 1915.00, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2025-09-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 8), 2884, '2025-09-10', '2025-09-15', 5, 1625.00, 45.00, 162.50, 1832.50, 'CONFIRMED', 'PAID'),
(uuid_generate_v4(), (SELECT id FROM public.auctions WHERE property_id=5 AND start_date='2025-11-01'), 5, (SELECT id FROM guest_cycle WHERE row_num = 9), 2884, '2025-11-05', '2025-11-12', 7, 1675.00, 45.00, 167.50, 1887.50, 'CONFIRMED', 'PAID');