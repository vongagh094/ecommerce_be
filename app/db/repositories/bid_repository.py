from app.db.models.Bid import Bids
from app.schemas.BidDTO import BidsDTO
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import Optional, Tuple, Any


class BidRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_existing_user_bid_for_auction(self, user_id: int, auction_id: str) -> Optional[Bids]:
        """Get existing ACTIVE bid by user for specific auction"""
        return self.db.query(Bids).filter(
            and_(
                Bids.user_id == user_id,
                Bids.auction_id == auction_id,
                Bids.status == 'ACTIVE'
            )
        ).first()

    def create_new_bid(self, bids_dto: BidsDTO) -> Bids:
        """Create new bid from DTO with proper field mapping"""
        new_bid = Bids(
            auction_id=bids_dto.auction_id,
            user_id=bids_dto.user_id,
            check_in=datetime.fromisoformat(bids_dto.check_in),
            check_out=datetime.fromisoformat(bids_dto.check_out),
            total_amount=bids_dto.bid_amount,
            allow_partial=bids_dto.allow_partial,
            partial_awarded=bids_dto.partial_awarded,
            bid_time=datetime.fromisoformat(bids_dto.bid_time),
            status="ACTIVE"
        )

        self.db.add(new_bid)
        self.db.commit()
        self.db.refresh(new_bid)
        return new_bid

    def update_existing_bid(self, existing_bid: Bids, bids_dto: BidsDTO) -> Bids:
        """Update existing bid with data from DTO"""
        existing_bid.check_in = datetime.fromisoformat(bids_dto.check_in)
        existing_bid.check_out = datetime.fromisoformat(bids_dto.check_out)
        existing_bid.total_amount = bids_dto.bid_amount
        existing_bid.allow_partial = bids_dto.allow_partial
        existing_bid.partial_awarded = bids_dto.partial_awarded
        existing_bid.bid_time = datetime.fromisoformat(bids_dto.bid_time)
        existing_bid.updated_at = datetime.now()

        self.db.commit()
        self.db.refresh(existing_bid)
        return existing_bid

    def upsert_user_bid(self, bids_dto: BidsDTO) -> Tuple[Bids, bool]:
        """
        Update existing bid or insert new one
        Returns: (bid_record, was_created)
        """
        existing_bid = self.get_existing_user_bid_for_auction(
            bids_dto.user_id,
            bids_dto.auction_id
        )

        if existing_bid:
            updated_bid = self.update_existing_bid(existing_bid, bids_dto)
            return updated_bid, False
        else:
            new_bid = self.create_new_bid(bids_dto)
            return new_bid, True

    def rollback(self):
        """Rollback the current transaction."""
        self.db.rollback()

    def get_active_bids_by_auction(self,auction_id: str) -> list[type[Bids]]:
        """Get all active bids for a specific auction"""
        return self.db.query(Bids).filter(
            and_(
                Bids.auction_id == auction_id,
                Bids.status == 'ACTIVE'
            )
        ).all()