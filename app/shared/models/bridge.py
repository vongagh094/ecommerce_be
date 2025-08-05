"""Bridge between existing models and new shared models."""

# Import existing models to maintain compatibility
from ...db.models.basic import BasicModel
from ...db.models.auction import AuctionDB as ExistingAuction
from ...db.models.Bid import Bids as ExistingBid

# Re-export for compatibility
__all__ = [
    "BasicModel",
    "ExistingAuction", 
    "ExistingBid"
]