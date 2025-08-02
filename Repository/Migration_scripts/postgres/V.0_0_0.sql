-- Trigger catch insert bid
CREATE OR REPLACE FUNCTION after_bids_insert()
    RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO bid_events ( auction_id, event_type, user_id, bid_id, event_data, event_time, created_at, updated_at)
    VALUES (
        NEW.auction_id,
        'bid_placed',
        NEW.user_id,
        NEW.id,
        jsonb_build_object('status', NEW.status),
        NEW.created_at,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_bids_insert_event
    AFTER INSERT ON bids
    FOR EACH ROW
EXECUTE FUNCTION after_bids_insert();

-- Trigger catch update bid
CREATE OR REPLACE FUNCTION after_bids_update()
    RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO bid_events ( auction_id, event_type, user_id, bid_id, event_data, event_time, created_at, updated_at)
    VALUES (
        NEW.auction_id,
        'bid_update',
        NEW.user_id,
        NEW.id,
        jsonb_build_object('status', NEW.status),
        NEW.created_at,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_bids_update_event
    AFTER UPDATE ON bids
    FOR EACH ROW
EXECUTE FUNCTION after_bids_update();