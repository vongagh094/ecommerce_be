from app.db.models.Bid import Bids
from app.db.models.auction import AuctionDB
from sqlalchemy.orm import Session


class BidRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_bid(self, bid: Bids):
        """Create a new bid in the database."""
        self.db.add(bid)
        self.db.commit()
        self.db.refresh(bid)
        return bid
    def get_bid_by_id(self, bid_id: str):
        """Retrieve a bid by its ID."""
        return self.db.query(Bids).filter(Bids.id == bid_id).first()
    def get_bid_by_user_id(self, user_id: str):
        """Retrieve a bid by user ID."""
        return self.db.query(Bids).filter(Bids.user_id == user_id).all()
    def get_bids_by_auction_id(self, auction_id: str):
        """Retrieve all bids for a specific auction."""
        return self.db.query(Bids).filter(Bids.auction_id == auction_id).all()

    def get_existing_bid(self, user_id: str, auction_id: str):
        """Check if a bid exists for a user on a specific auction."""
        return self.db.query(Bids).filter(
            Bids.user_id == user_id,
            Bids.auction_id == auction_id
        ).first()
    def get_highest_bid_for_auction(self, auction_id: str):
        """Retrieve the highest bid for a specific auction."""
        return self.db.query(Bids).filter(Bids.auction_id == auction_id).order_by(Bids.bid_amount.desc()).first()
    def update_bid(self, bid: Bids):
        """Update an existing bid."""
        existing_bid = self.get_bid_by_id(bid.id)
        if existing_bid:
            for key, value in bid.__dict__.items():
                if value is not None and key != 'id':
                    setattr(existing_bid, key, value)
            self.db.commit()
            self.db.refresh(existing_bid)
            return existing_bid
        return None
    def delete_bid(self, bid_id: str):
        """Delete a bid by its ID."""
        bid = self.get_bid_by_id(bid_id)
        if bid:
            self.db.delete(bid)
            self.db.commit()
            return True
        return False

    def rollback(self):
        """Rollback the current transaction."""
        self.db.rollback()




