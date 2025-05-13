from enum import Enum
from typing import Optional
from pydantic import BaseModel

class PaymentMethodType(Enum):
    CASH = "cash"
    CARD = "card"

class PaymentMethod(BaseModel):
    method: PaymentMethodType
    card: Optional[str] = None