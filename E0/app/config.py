import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://macaceres2:hJkpukibu534@db:5432/stock_market")
    #??? está bien?¿?

settings = Settings()