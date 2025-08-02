INSERT INTO users (
    id, email, username, password_hash, full_name,
    first_name, last_name, profile_image_url, verification_status,
    is_active, is_admin, is_super_host,
    host_about, host_review_count, host_rating_average
) VALUES (
    1, 'demo@example.com', 'demo_user', 'hashed_password_here', 'Demo User',
    'Demo', 'User', 'https://example.com/profile.jpg', 'VERIFIED',
    TRUE, FALSE, TRUE,
    'Experienced host with multiple listings.', 42, 4.85
);
INSERT INTO properties (
    id,host_id, title, description, property_type, category,
    max_guests, bedrooms, bathrooms, address_line1, city, state,
    country, postal_code, latitude, longitude, base_price,
    cleaning_fee, cancellation_policy, instant_book, minimum_stay,
    home_tier, is_guest_favorite, language, status
) VALUES (
    1,1, 'Cozy Apartment in City Center', 'A comfortable 2-bedroom apartment in the heart of the city.',
    'Apartment', 'Entire Place', 4, 2, 1, '123 Main St', 'Sample City', 'Sample State',
    'Sample Country', '12345', 10.762622, 106.660172, 100.00,
    15.00, 'Flexible', TRUE, 2, 1, TRUE, 'en', 'ACTIVE'
);

INSERT INTO auctions (
    id, property_id, start_date, end_date,
    min_nights, max_nights, starting_price, current_highest_bid,
    bid_increment, minimum_bid, auction_start_time, auction_end_time,
    objective, status, winner_user_id, total_bids
) VALUES (
    '22222222-2222-2222-2222-222222222222', 1, '2025-08-01', '2025-08-05',
    1, 5, 200.00, NULL,
    10.00, 200.00, '2025-08-01 09:00:00', '2025-08-01 21:00:00',
    'HIGHEST_TOTAL', 'PENDING', 1, 0
);
