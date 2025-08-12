# Import all models here to ensure they're registered with SQLAlchemy
from .user import User
from .property import Property
from .property_type import PropertyType
from .property_category import PropertyCategory
from .property_image import PropertyImage
from .property_amenity import PropertyAmenity
from .amenity import Amenity
from .conversation import Conversation
from .message import Message
from .wishlist import Wishlist
from .wishlist_property import WishlistProperty
from .auction import AuctionDB
from .Bid import Bids
from .property_extras import PropertyHighlight, HouseRule, LocationDescription

__all__ = [
    "User",
    "Property", 
    "PropertyType",
    "PropertyCategory",
    "PropertyImage",
    "PropertyAmenity",
    "Amenity",
    "Conversation",
    "Message",
    "Wishlist",
    "WishlistProperty",
    "AuctionDB",
    "Bids",
    "PropertyHighlight",
    "HouseRule",
    "LocationDescription",
]