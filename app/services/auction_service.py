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
                print(f"Auction with id {auction_id} not found.")
                return None

            if highest_bid is not None:
                self.auction_repository.update_auction(
                    auction_id, {"current_highest_bid": highest_bid}
                )
                return self.auction_repository.get_auction_by_id(auction_id)
            else:
                print("Invalid highest_bid value.")
                return None

        except Exception as e:
            print(f"Error updating highest bid auction service: {e}")
            return None


