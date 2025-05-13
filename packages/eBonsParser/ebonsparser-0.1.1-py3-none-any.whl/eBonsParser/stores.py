from eBonsParser.models.base import *

class Rewe(Store):
    """
    Represents a Rewe Supermarket.
    """
    name: str = Field(default="REWE Markt GmbH")
    type: StoreType = Field(default=StoreType.SUPERMARKET)


class Thalia(Store):
    """
    Represents a Thalia Library.
    """
    name: str = Field(default="Thalia")
    type: StoreType = Field(default=StoreType.LIBRARY)
