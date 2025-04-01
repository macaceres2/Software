from fastapi import FastAPI, Query, HTTPException, Depends
from typing import Optional
from datetime import datetime
from .models import Stock, StockResponse, StocksList
from .database import save_stock, get_stocks, get_stock_by_symbol
from .mqtt_client import mqtt_client
import uvicorn
import threading
import time

app = FastAPI(
    title = "Stock Market Async",
    description = "API de manejo de stocks",
    version = "1.0.0"
)

#avanzada
@app.on_event("startup")
async def startup_event():
    threading.Thread(target=mqtt_client.connect, daemon=True).start()
    print("Cliente iniciado")  
@app.on_event("shutdown")
async def shutdown_event():
    mqtt_client.disconnect()
    print("Cliente desconectado")

@app.get("/", tags = ["Home"])
def home():
    return {"message": "API funcionando"}

@app.get("/stocks", response_model=StocksList, tags=["Stocks"])
def list_stocks(
    price:Optional[float] = Query(None, description="Filtrar por precio menor o igual"),
    quantity:Optional[float] = Query(None, description="Filtrar por cantidad menor o igual a este valor"),
    date:Optional[str] = Query(None, description="Filtrar por fecha YYY-MM-DD"),
    page:int = Query(1, ge=1, description="Número de página"),
    count: int = Query(25, ge=1, le=30, description="Cantidad de elementos por página")
):
    stocks, total = get_stocks(price, quantity, date, page, count)

    return {
        "items": stocks,
        "metadata": {
            "page": page,
            "count": count,
            "total": total,
            "pages": (total + count - 1) // count
        }
    }

@app.get("/stocks/{symbol}", response_model=StocksList, tags=["Stocks"])
def get_stock(
    symbol: str,
    price: Optional[float] = Query(None, description="Filtrar por precio menor o igual a este valor"),
    quantity: Optional[int] = Query(None, description="Filtrar por cantidad menor o igual a este valor"),
    date: Optional[str] = Query(None, description="Filtrar por fecha exacta (formato YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Número de página"),
    count: int = Query(25, ge=1, le=30, description="Cantidad de elementos por página")
):
    stocks, total = get_stock_by_symbol(symbol, price, quantity, date, page, count)
    
    if total == 0:
        raise HTTPException(status_code=404, detail=f"No se encontraron stocks para el símbolo {symbol} con los filtros proporcionados")
    
    return {
        "items": stocks,
        "metadata": {
            "page": page,
            "count": count,
            "total": total,
            "pages": (total + count - 1) // count
        }
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)