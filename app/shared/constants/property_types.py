"""Property type constants."""

from enum import Enum


class PropertyType(str, Enum):
    """Property type enumeration."""
    APARTMENT = "apartment"
    HOUSE = "house"
    CABIN = "cabin"
    VILLA = "villa"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    LOFT = "loft"
    STUDIO = "studio"


class PropertyCategory(str, Enum):
    """Property category enumeration."""
    AMAZING_VIEWS = "amazing_views"
    CABINS = "cabins"
    FAMILY = "family"
    BEACHFRONT = "beachfront"
    LUXURY = "luxury"
    UNIQUE_STAYS = "unique_stays"
    COUNTRYSIDE = "countryside"
    CITY_CENTER = "city_center"