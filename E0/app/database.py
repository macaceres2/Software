from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://macaceres2:hJkpukibu534@db:5432/stock_market"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class StockDB(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    shortName = Column(String)
    longName = Column(String)
    quantity = Column(Integer)
    timestamp = Column(DateTime)

Base.metadata.create_all(bind=engine)

def save_stock(stock_data):
    db = SessionLocal()
    stock = StockDB(
        symbol=stock_data["symbol"],
        price=stock_data["price"],
        shortName=stock_data["shortName"],
        longName=stock_data["longName"],
        quantity=stock_data["quantity"],
        timestamp=datetime.fromisoformat(stock_data["timestamp"])
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)
    db.close()

def get_stocks(price=None, quantity=None, date=None, page=1, count=25):
    db = SessionLocal()
    query = db.query(StockDB)

    if price:
        query = query.filter(StockDB.price <= price)
    if quantity:
        query = query.filter(StockDB.quantity <= quantity)
    if date:
        query = query.filter(StockDB.timestamp.cast(String).startswith(date))

    stocks = query.offset((page - 1) * count).limit(count).all()
    db.close()
    return stocks

def get_stock_by_symbol(symbol, price=None, quantity=None, date=None):
    db = SessionLocal()
    query = db.query(StockDB).filter(StockDB.symbol == symbol)

    if price:
        query = query.filter(StockDB.price <= price)
    if quantity:
        query = query.filter(StockDB.quantity <= quantity)
    if date:
        query = query.filter(StockDB.timestamp.cast(String).startswith(date))

    stock = query.first()
    db.close()
    return stock