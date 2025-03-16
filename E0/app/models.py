from pydantic import BaseModel

class Stock(BaseModel):
    symbol: str
    price: float
    shortName: str
    longName: str
    quantity: int
    timestamp: str