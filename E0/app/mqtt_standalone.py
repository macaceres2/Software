"""
Script independiente para iniciar el cliente MQTT.
Se ejecuta como un servicio separado en Docker.
"""
import sys
import os
import time
import json
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configuración de variables de entorno
DATABASE_HOST = os.getenv("DATABASE_HOST", "db")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_USER = os.getenv("DATABASE_USER", "macaceres2")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "hJkpukibu534")
DATABASE_NAME = os.getenv("DATABASE_NAME", "stock_market")
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "stocks/info")

# Configuración de SQLAlchemy
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

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Función para guardar el stock en la base de datos
def save_stock(stock_data):
    db = SessionLocal()
    try:
        timestamp = stock_data["timestamp"]
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
            
        stock = StockDB(
            symbol=stock_data["symbol"],
            price=stock_data["price"],
            shortName=stock_data["shortName"],
            longName=stock_data["longName"],
            quantity=stock_data["quantity"],
            timestamp=timestamp
        )
        db.add(stock)
        db.commit()
        db.refresh(stock)
        print(f"Stock guardado: {stock.symbol} a ${stock.price}")
        return stock
    except Exception as e:
        db.rollback()
        print(f"Error al guardar stock: {e}")
    finally:
        db.close()

# Callbacks MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Conectado al broker MQTT {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"Suscrito al tema: {MQTT_TOPIC}")
    else:
        print(f"Error de conexión al broker MQTT, código {rc}")

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        print(f"Mensaje recibido en {message.topic}: {payload}")
        stock_data = json.loads(payload)

        if all(key in stock_data for key in ["symbol", "price", "shortName", "longName", "quantity", "timestamp"]):
            save_stock(stock_data)
        else:
            print(f"Mensaje MQTT con formato inválido: {payload}")
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON: {payload}")
    except Exception as e:
        print(f"Error al procesar el mensaje MQTT: {e}")

def main():
    print("Iniciando cliente MQTT independiente...")
    
    # Crear cliente MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Conectar al broker
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        # Iniciar el loop en modo bloquante
        client.loop_forever()
    except KeyboardInterrupt:
        print("Cerrando cliente MQTT...")
        client.disconnect()
    except Exception as e:
        print(f"Error en el cliente MQTT: {e}")
        time.sleep(10)  # Esperar antes de reintentar
        main()  # Reintentar conexión

if __name__ == "__main__":
    main()