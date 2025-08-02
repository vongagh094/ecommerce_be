from app.schemas.BidDTO import BidsDTO
from app.db.repositories.bid_repository import BidRepository
from app.db.models.Bid import Bids
class BidService:
    def __init__(self, bid_repository: BidRepository):
        self.bid_repository = bid_repository

    def place_bids(self, bid_data:dict):
        """Place a bid on an auction."""
        try:
            existing_bid = self.bid_repository.get_existing_bid(bid_data.get("user_id"),bid_data.get("auction_id"))
            if existing_bid:
                #Update the existing bid
                existing_bid.total_amount = bid_data.get("bid_amount")
                existing_bid.bid_time = bid_data.get("bid_time")
                existing_bid.updated_at = bid_data.get("created_at")
                existing_bid.status = bid_data.get("status", "active")
                existing_bid.check_in = bid_data.get("check_in")
                existing_bid.check_out = bid_data.get("check_out")
                existing_bid.allow_partial = bid_data.get("allow_partial")

                return self.bid_repository.update_bid(existing_bid)
            else:
                # Create a new bid
                new_bid = Bids(
                    auction_id=bid_data.get("auction_id"),
                    user_id=bid_data.get("user_id"),
                    bid_time=bid_data.get("bid_time"),
                    status=bid_data.get("status", "active"),
                    total_amount= bid_data.get("bid_amount"),
                    check_in = bid_data.get("check_in"),
                    check_out = bid_data.get("check_out"),
                    allow_partial = bid_data.get("allow_partial")
                )
                return self.bid_repository.create_bid(new_bid)
        except Exception as e:
            self.bid_repository.rollback()
            print(f"Error updating database bid service: {e}")
            return None
