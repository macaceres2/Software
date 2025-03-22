import os

class Settings:
    # Obtener variables de entorno con valores por defecto para desarrollo
    DATABASE_HOST = os.getenv("DATABASE_HOST", "db")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_USER = os.getenv("DATABASE_USER", "macaceres2")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "hJkpukibu534")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "stock_market")
    
    # Construir URL de conexión
    DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    
    # Configuración MQTT
    MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    MQTT_TOPIC = os.getenv("MQTT_TOPIC", "stocks/info")

settings = Settings()