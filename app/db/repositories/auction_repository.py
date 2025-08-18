from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.models.auction import Auction
from app.schemas.AuctionDTO import AuctionCreateDTO
import logging

logger = logging.getLogger(__name__)

class AuctionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_auction(self, data: AuctionCreateDTO) -> Auction:
        """Create a new auction."""
        try:
            from datetime import datetime
            # Chuyển auction_start_time và auction_end_time thành timestamp
            start_time = datetime.strptime(data.auction_start_time, "%H:%M").time()
            end_time = datetime.strptime(data.auction_end_time, "%H:%M").time()
            # Kết hợp với start_date để tạo timestamp
            auction_start = datetime.combine(data.start_date, start_time)
            auction_end = datetime.combine(data.end_date, end_time)

            new_auction = Auction(
                property_id=data.property_id,
                start_date=data.start_date,
                end_date=data.end_date,
                min_nights=data.min_nights,
                max_nights=data.max_nights,
                starting_price=data.starting_price,
                bid_increment=data.bid_increment,
                minimum_bid=data.minimum_bid,
                auction_start_time=auction_start,
                auction_end_time=auction_end,
                objective=data.objective,
                status="PENDING",
                total_bids=0
            )
            self.db.add(new_auction)
            self.db.commit()
            self.db.refresh(new_auction)
            return new_auction
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error in create_auction: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"Invalid time format in create_auction: {str(e)}")
            raise

    def get_auction_by_id(self, auction_id: str) -> Optional[Auction]:
        """Get an auction by its ID."""
        return self.db.query(Auction).filter(Auction.id == auction_id).first()

    def get_all_auctions(self) -> List[Auction]:
        """Get all auctions."""
        return self.db.query(Auction).all()

    def get_auctions_by_property(self, property_id: int) -> List[Auction]:
        """Get all auctions for a specific property."""
        return self.db.query(Auction).filter(Auction.property_id == property_id).all()

    def update_auction(self, auction_id: str, auction_data: dict) -> Optional[Auction]:
        """Update an existing auction."""
        try:
            auction = self.get_auction_by_id(auction_id)
            if auction:
                for key, value in auction_data.items():
                    setattr(auction, key, value)
                self.db.commit()
                self.db.refresh(auction)
                return auction
            return None
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error in update_auction: {str(e)}")
            raise

    def update_auction_status(self, auction_id: str, status: str) -> Optional[Auction]:
        """Update the status of an auction."""
        try:
            auction = self.get_auction_by_id(auction_id)
            if auction:
                auction.status = status
                self.db.commit()
                self.db.refresh(auction)
                return auction
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error in update_auction_status: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error updating auction status: {str(e)}")
            return None
    def delete_auction(self, auction_id: str) -> bool:
        """Delete an auction by its ID."""
        try:
            auction = self.get_auction_by_id(auction_id)
            if auction:
                self.db.delete(auction)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error in delete_auction: {str(e)}")
            raise