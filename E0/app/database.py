from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import settings


engine = create_engine(settings.DATABASE_URL)
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_stock(stock_data):
    db = SessionLocal()
    try:

        timestamp = stock_data["timestamp"]
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        stock = StockDB(
            symbol = stock_data["symbol"],
            price = stock_data["price"],
            shortName = stock_data["shortName"],
            longName = stock_data["longName"],
            quantity = stock_data["quantity"],
            timestamp = timestamp
        )
        db.add(stock)
        db.commit()
        db.refresh(stock)
        return stock
    
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_stocks(price=None, quantity=None, date=None, page=1, count=25):
    db = SessionLocal()
    try:
        query = db.query(StockDB)

        if price is not None:
            query = query.filter(StockDB.price <= price)
        if quantity is not None:
            query = query.filter(StockDB.quantity <= quantity)
        if date is not None:
            query = query.filter(func.date(StockDB.timestamp) == date)
        
        total = query.count()

        stocks = query.order_by(StockDB.timestamp.desc()).offset((page - 1) * count).limit(count).all()

        return stocks, total
    
    finally:
        db.close()

def get_stock_by_symbol(symbol, price=None, quantity=None, date=None, page=1, count=25):
    db = SessionLocal()
    try:
        query = db.query(StockDB).filter(StockDB.symbol == symbol)
        if price is not None:
            query = query.filter(StockDB.price <= price)
        if quantity is not None:
            query = query.filter(StockDB.quantity <= quantity)
        if date is not None:
            query = query.filter(func.date(StockDB.timestamp) == date)

        total = query.count()
        stocks = query.order_by(StockDB.timestamp.desc()).offset((page - 1) * count).limit(count).all()

        return stocks, total
    finally:
        db.close()