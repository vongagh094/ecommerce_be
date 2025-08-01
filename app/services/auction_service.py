from app.db.repositories.auction_repository import AuctionRepository
class AuctionService:
    def __init__(self, auction_repository: AuctionRepository):
        """ Initialize the AuctionService with a repository."""
        self.auction_repository = auction_repository
    def update_highest_bid(self, auction_id: str, highest_bid: float):
        """Update the highest bid for an auction."""
        try:
            auction = self.auction_repository.get_auction_by_id(auction_id)
            if not auction:
                return None
            if highest_bid:
                auction.highest_bid = highest_bid
                self.auction_repository.update_auction(auction_id, {"highest_bid": highest_bid})
                return auction
            else:
                return None
        except Exception as e:
            print(f"Error updating highest bid auction service: {e}")
            return None

