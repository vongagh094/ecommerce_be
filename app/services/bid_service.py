from app.db.repositories.bid_repository import BidRepository
from typing import Dict, Optional
from app.schemas.BidDTO import BidsDTO


class BidService:
    def __init__(self, bid_repository: BidRepository):
        self.bid_repository = bid_repository

    def place_bid(self, bids_dto: BidsDTO) -> Dict:
        """
        Place bid using correct DTO → Model mapping
        - Check if user has existing bid for this auction
        - UPDATE if exists, INSERT if not
        """
        try:
            # UPSERT bid (update existing or insert new)
            bid_record, was_created = self.bid_repository.upsert_user_bid(bids_dto)

            if bid_record:
                action = "created" if was_created else "updated"
                return {
                    "success": True,
                    "bid_id": str(bid_record.id),
                    "action": action,
                    "user_id": bid_record.user_id,
                    "auction_id": bid_record.auction_id,
                    "total_amount": bid_record.total_amount,  # INT from DB
                    "price_per_night": bid_record.price_per_night,  # INT computed by DB
                    "nights": bid_record.nights,  # INT computed by DB
                    "check_in": bid_record.check_in.isoformat(),
                    "check_out": bid_record.check_out.isoformat(),
                    "bid_time": bid_record.bid_time.isoformat(),
                    "allow_partial": bid_record.allow_partial,
                    "partial_awarded": bid_record.partial_awarded,
                    "status": bid_record.status,
                    "message": f"Bid {action} successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to save bid"
                }

        except Exception as e:
            self.bid_repository.rollback()
            print(f"Error in place_bid: {e}")
            return {
                "success": False,
                "message": f"Error placing bid: {str(e)}"
            }

    def get_user_current_bid(self, user_id: int, auction_id: str) -> Optional[Dict]:
        """Get user's current active bid for an auction"""
        try:
            existing_bid = self.bid_repository.get_existing_user_bid_for_auction(user_id, auction_id)

            if not existing_bid:
                return None

            return {
                "bid_id": str(existing_bid.id),
                "user_id": existing_bid.user_id,
                "auction_id": existing_bid.auction_id,
                "total_amount": existing_bid.total_amount,  # INT
                "price_per_night": existing_bid.price_per_night,  # INT
                "nights": existing_bid.nights,  # INT
                "check_in": existing_bid.check_in.isoformat(),
                "check_out": existing_bid.check_out.isoformat(),
                "bid_time": existing_bid.bid_time.isoformat(),
                "allow_partial": existing_bid.allow_partial,
                "partial_awarded": existing_bid.partial_awarded,
                "status": existing_bid.status,
                "created_at": existing_bid.created_at.isoformat(),
                "updated_at": existing_bid.updated_at.isoformat()
            }

        except Exception as e:
            print(f"Error getting user current bid: {e}")
            return None