-- ===================================================================
-- INSERT SAMPLE DATA FOR AUCTIONS AND BOOKINGS TABLES
-- ===================================================================

-- First, let's insert additional sample users if needed
INSERT INTO users (id, email, username, full_name, first_name, last_name, verification_status, is_active, created_at, updated_at) VALUES
(500001, 'guest1@example.com', 'guest_user_1', 'Alice Johnson', 'Alice', 'Johnson', 'VERIFIED', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(500002, 'guest2@example.com', 'guest_user_2', 'Bob Smith', 'Bob', 'Smith', 'VERIFIED', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(500003, 'guest3@example.com', 'guest_user_3', 'Carol Williams', 'Carol', 'Williams', 'VERIFIED', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(500004, 'guest4@example.com', 'guest_user_4', 'David Brown', 'David', 'Brown', 'VERIFIED', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(500005, 'guest5@example.com', 'guest_user_5', 'Emma Davis', 'Emma', 'Davis', 'VERIFIED', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ===================================================================
-- AUCTIONS TABLE INSERTS
-- ===================================================================

-- Auction 1: Paris Zen Apartment (Property ID: 3109)
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '11111111-1111-1111-1111-111111111111', 3109, '2025-08-15', '2025-08-20',
    2, 5, 50.00, 65.00, 5.00, 50.00,
    '2025-08-10 10:00:00', '2025-08-14 18:00:00', 'HIGHEST_TOTAL', 'ACTIVE', NULL, 3
);

-- Auction 2: Amazing Loft in Paris (Property ID: 11798)
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '22222222-2222-2222-2222-222222222222', 11798, '2025-08-18', '2025-08-25',
    3, 7, 70.00, 85.00, 5.00, 70.00,
    '2025-08-12 09:00:00', '2025-08-17 20:00:00', 'HIGHEST_PER_NIGHT', 'COMPLETE', NULL, 5
);

-- Auction 3: Sydney Rooftop Apartment (Property ID: 15253)
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '33333333-3333-3333-3333-333333333333', 15253, '2025-09-01', '2025-09-07',
    2, 6, 80.00, NULL, 10.00, 80.00,
    '2025-08-25 08:00:00', '2025-08-30 19:00:00', 'HYBRID', 'PENDING', NULL, 0
);

-- Auction 4: NYC East Village Room (Property ID: 16580) - COMPLETED
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '44444444-4444-4444-4444-444444444444', 16580, '2025-08-01', '2025-08-05',
    1, 4, 60.00, 90.00, 5.00, 60.00,
    '2025-07-25 10:00:00', '2025-07-31 22:00:00', 'HIGHEST_TOTAL', 'COMPLETED', 500001, 7
);

-- Auction 5: St Michel Elegance (Property ID: 16626) - COMPLETED
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '55555555-5555-5555-5555-555555555555', 16626, '2025-07-20', '2025-07-25',
    2, 5, 100.00, 130.00, 10.00, 100.00,
    '2025-07-15 11:00:00', '2025-07-19 21:00:00', 'HIGHEST_TOTAL', 'COMPLETED', 500002, 8
);

-- Auction 6: Future auction for Paris Zen (different dates)
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '66666666-6666-6666-6666-666666666666', 3109, '2025-09-10', '2025-09-15',
    1, 5, 55.00, NULL, 5.00, 55.00,
    '2025-09-05 12:00:00', '2025-09-09 18:00:00', 'HIGHEST_PER_NIGHT', 'PENDING', NULL, 0
);
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '77777777-7777-7777-7777-777777777777', 11798, '2025-09-1', '2025-09-15',
    1, 5, 55.00, NULL, 5.00, 55.00,
    '2025-08-25 12:00:00', '2025-08-29 18:00:00', 'HIGHEST_PER_NIGHT', 'PENDING', NULL, 0
);
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '88888888-8888-8888-8888-888888888888', 11798, '2025-08-25', '2025-08-31',
    1, 5, 55.00, NULL, 5.00, 55.00,
    '2025-08-18 07:00:00', '2025-08-24 18:00:00', 'HIGHEST_PER_NIGHT', 'ACTIVE', NULL, 0
);
INSERT INTO auctions (
    id, property_id, start_date, end_date, min_nights, max_nights,
    starting_price, current_highest_bid, bid_increment, minimum_bid,
    auction_start_time, auction_end_time, objective, status, winner_user_id, total_bids
) VALUES (
    '99999999-9999-9999-9999-999999999999', 11798, '2025-09-16', '2025-09-30',
    1, 5, 55.00, NULL, 5.00, 55.00,
    '2025-08-18 07:00:00', '2025-08-18 12:50:00', 'HIGHEST_PER_NIGHT', 'ACTIVE', NULL, 0
);

-- ===================================================================
-- BOOKINGS TABLE INSERTS
-- ===================================================================

-- Booking 1: From completed auction (NYC East Village)
INSERT INTO bookings (
    id, auction_id, property_id, guest_id, host_id,
    check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount,
    booking_status, payment_status
) VALUES (
    '10000001-1000-1000-1000-100000000001', '44444444-4444-4444-4444-444444444444',
    16580, 500001, 64442, '2025-08-01', '2025-08-05', 4,
    360.00, 25.00, 30.60, 415.60,
    'CONFIRMED', 'COMPLETED'
);

-- Booking 2: From completed auction (St Michel Elegance)
INSERT INTO bookings (
    id, auction_id, property_id, guest_id, host_id,
    check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount,
    booking_status, payment_status
) VALUES (
    '10000002-1000-1000-1000-100000000002', '55555555-5555-5555-5555-555555555555',
    16626, 500002, 64627, '2025-07-20', '2025-07-25', 5,
    650.00, 40.00, 55.20, 745.20,
    'CONFIRMED', 'COMPLETED'
);

-- Booking 3: Direct booking (not from auction) - Paris Loft
INSERT INTO bookings (
    id, auction_id, property_id, guest_id, host_id,
    check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount,
    booking_status, payment_status
) VALUES (
    '10000003-1000-1000-1000-100000000003', NULL,
    11798, 500003, 44444, '2025-08-10', '2025-08-13', 3,
    210.00, 20.00, 18.40, 248.40,
    'CONFIRMED', 'PENDING'
);

-- Booking 4: Direct booking - Sydney Apartment
INSERT INTO bookings (
    id, auction_id, property_id, guest_id, host_id,
    check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount,
    booking_status, payment_status
) VALUES (
    '10000004-1000-1000-1000-100000000004', NULL,
    15253, 500004, 59850, '2025-08-25', '2025-08-28', 3,
    240.00, 30.00, 21.60, 291.60,
    'PENDING', 'PENDING'
);

-- Booking 5: Future booking from potential auction win
INSERT INTO bookings (
    id, auction_id, property_id, guest_id, host_id,
    check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount,
    booking_status, payment_status
) VALUES (
    '10000005-1000-1000-1000-100000000005', NULL,
    3109, 500005, 3631, '2025-09-01', '2025-09-04', 3,
    180.00, 15.00, 15.60, 210.60,
    'PENDING', 'PENDING'
);

-- Booking 6: Cancelled booking example
INSERT INTO bookings (
    id, auction_id, property_id, guest_id, host_id,
    check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount,
    booking_status, payment_status
) VALUES (
    '10000006-1000-1000-1000-100000000006', NULL,
    11798, 500001, 44444, '2025-07-15', '2025-07-18', 3,
    210.00, 20.00, 18.40, 248.40,
    'CANCELLED', 'REFUNDED'
);

-- Booking 7: Upcoming booking from auction
INSERT INTO bookings (
    id, auction_id, property_id, guest_id, host_id,
    check_in_date, check_out_date, total_nights,
    base_amount, cleaning_fee, taxes, total_amount,
    booking_status, payment_status
) VALUES (
    '10000007-1000-1000-1000-100000000007', '22222222-2222-2222-2222-222222222222',
    11798, 500003, 44444, '2025-08-18', '2025-08-21', 3,
    255.00, 20.00, 22.00, 297.00,
    'CONFIRMED', 'COMPLETED'
);

-- ===================================================================
-- BIDS TABLE INSERTS (Related to active auctions)
-- ===================================================================

-- Bids for Auction 1 (Paris Zen Apartment)
INSERT INTO bids (
    id, auction_id, user_id, check_in, check_out,
    total_amount, allow_partial, partial_awarded, status
) VALUES
('b0000001-0000-0000-0000-000000000001', '11111111-1111-1111-1111-111111111111', 500001, '2025-08-15', '2025-08-18', 180.00, true, false, 'ACTIVE'),
('b0000002-0000-0000-0000-000000000002', '11111111-1111-1111-1111-111111111111', 500002, '2025-08-16', '2025-08-20', 260.00, true, false, 'ACTIVE'),
('b0000003-0000-0000-0000-000000000003', '11111111-1111-1111-1111-111111111111', 500003, '2025-08-15', '2025-08-20', 325.00, true, false, 'ACTIVE');

-- Bids for Auction 2 (Amazing Loft in Paris)
INSERT INTO bids (
    id, auction_id, user_id, check_in, check_out,
    total_amount, allow_partial, partial_awarded, status
) VALUES
('b0000004-0000-0000-0000-000000000004', '22222222-2222-2222-2222-222222222222', 500004, '2025-08-18', '2025-08-22', 340.00, true, false, 'ACTIVE'),
('b0000005-0000-0000-0000-000000000005', '22222222-2222-2222-2222-222222222222', 500005, '2025-08-20', '2025-08-25', 425.00, true, false, 'ACTIVE'),
('b0000006-0000-0000-0000-000000000006', '22222222-2222-2222-2222-222222222222', 500001, '2025-08-18', '2025-08-25', 595.00, true, false, 'ACTIVE'),
('b0000007-0000-0000-0000-000000000007', '22222222-2222-2222-2222-222222222222', 500002, '2025-08-19', '2025-08-24', 425.00, true, false, 'ACTIVE'),
('b0000008-0000-0000-0000-000000000008', '22222222-2222-2222-2222-222222222222', 500003, '2025-08-18', '2025-08-23', 425.00, true, false, 'ACTIVE');

-- Historical bids for completed auctions
INSERT INTO bids (
    id, auction_id, user_id, check_in, check_out,
    total_amount, allow_partial, partial_awarded, status
) VALUES
('b0000009-0000-0000-0000-000000000009', '44444444-4444-4444-4444-444444444444', 500001, '2025-08-01', '2025-08-05', 360.00, true, true, 'WON'),
('b0000010-0000-0000-0000-000000000010', '44444444-4444-4444-4444-444444444444', 500002, '2025-08-01', '2025-08-05', 340.00, true, false, 'OUTBID'),
('b0000011-0000-0000-0000-000000000011', '55555555-5555-5555-5555-555555555555', 500002, '2025-07-20', '2025-07-25', 650.00, true, true, 'WON'),
('b0000012-0000-0000-0000-000000000012', '55555555-5555-5555-5555-555555555555', 500001, '2025-07-20', '2025-07-25', 600.00, true, false, 'OUTBID');

-- ===================================================================
-- VERIFICATION QUERIES
-- ===================================================================

-- Check the inserted data
/*
-- View all auctions with property info
SELECT a.id, a.property_id, p.title, a.start_date, a.end_date,
       a.starting_price, a.current_highest_bid, a.status, a.total_bids
FROM auctions a
JOIN properties p ON a.property_id = p.id
ORDER BY a.created_at DESC;

-- View all bookings with guest and host info
SELECT b.id, p.title, g.full_name as guest_name, h.full_name as host_name,
       b.check_in_date, b.check_out_date, b.total_nights,
       b.total_amount, b.booking_status, b.payment_status
FROM bookings b
JOIN properties p ON b.property_id = p.id
JOIN users g ON b.guest_id = g.id
JOIN users h ON b.host_id = h.id
ORDER BY b.created_at DESC;

-- View bids with auction and user info
SELECT bd.id, a.property_id, p.title, u.full_name as bidder_name,
       bd.check_in, bd.check_out, bd.total_amount, bd.price_per_night, bd.status
FROM bids bd
JOIN auctions a ON bd.auction_id = a.id
JOIN properties p ON a.property_id = p.id
JOIN users u ON bd.user_id = u.id
ORDER BY a.property_id, bd.total_amount DESC;
*/
