from fastapi import FastAPI, Query
from datetime import datetime
from .models import Stock
from .database import save_stock, get_stocks, get_stock_by_symbol
from .mqtt_client import mqtt_client

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API funcionando"}

@app.post("/stocks")
def add_stock(stock: Stock):
    stock_dict = stock.dict()
    stock_dict["timestamp"] = datetime.now().isoformat()
    save_stock(stock_dict)
    return {"message": "Stock agregado correctamente", "data": stock_dict}

@app.get("/stocks")
def get_stocks(
    price: float = Query(None, alias="price"),
    quantity: int = Query(None, alias="quantity"),
    date: str = Query(None, alias="date"),
    page: int = Query(1, alias="page"),
    count: int = Query(25, alias="count")
):
    filtered_stocks = get_stocks(price, quantity, date, page, count)
    return {
        "stocks": filtered_stocks,
        "page": page,
        "count": count,
        "total": len(filtered_stocks)
    }

@app.get("/stocks/{symbol}")
def get_stock(
    symbol: str,
    price: float = Query(None, alias="price"),
    quantity: int = Query(None, alias="quantity"),
    date: str = Query(None, alias="date")
):
    stock = get_stock_by_symbol(symbol, price, quantity, date)
    if stock:
        return stock
    return {"error": "Stock no encontrado"}