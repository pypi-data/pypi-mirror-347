from enum import Enum
from typing import Optional
from pydantic import BaseModel

class TaxClass(Enum):
    REGULAR = 0.19
    REDUCED = 0.07
    EXEMPT = 0.0

class QuantityUnit(Enum):
    KG = "kg"
    G = "g"
    L = "l"
    ML = "ml"
    PCS = "pcs"

class Quantity(BaseModel):
    unit: QuantityUnit
    weight: Optional[float] = None

class Item(BaseModel):
    name: str
    price: float
    unit: Optional[str] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    tax_class: Optional[float] = None
