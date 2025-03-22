from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class Stock(BaseModel):
    symbol: str
    price: float
    shortName: str
    longName: str
    quantity: int
    timestamp: str
    
class StockResponse(BaseModel):
    id: int
    symbol: str
    price: float
    shortName: str
    longName: str
    quantity: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

class PaginationMetadata(BaseModel):
    page: int
    count: int
    total: int
    pages: int

class StocksList(BaseModel):
    items: List[StockResponse]
    metadata: PaginationMetadata