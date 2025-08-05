from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.auction import AuctionDB
class AuctionRepository:
    def __init__(self, db: Session):
        self.db = db
    def create_auction(self, auction_data: dict) -> AuctionDB:
        """Create a new auction."""
        new_auction = AuctionDB(**auction_data)
        self.db.add(new_auction)
        self.db.commit()
        self.db.refresh(new_auction)
        return new_auction
    def get_auction_by_id(self, auction_id: str) -> Optional[AuctionDB]:
        """Get an auction by its ID."""
        return self.db.query(AuctionDB).filter(AuctionDB.id == auction_id).first()
    def get_all_auctions(self) -> List[AuctionDB]:
        """Get all auctions."""
        return self.db.query(AuctionDB).all()

    def update_auction(self, auction_id: str, auction_data: dict) -> Optional[AuctionDB]:
        """Update an existing auction."""
        auction = self.get_auction_by_id(auction_id)
        if auction:
            for key, value in auction_data.items():
                setattr(auction, key, value)
            self.db.commit()
            self.db.refresh(auction)
            return auction
        return None
    def delete_auction(self, auction_id: str) -> bool:
        """Delete an auction by its ID."""
        auction = self.get_auction_by_id(auction_id)
        if auction:
            self.db.delete(auction)
            self.db.commit()
            return True
        return False
