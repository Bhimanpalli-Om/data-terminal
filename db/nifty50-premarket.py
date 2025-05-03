import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import requests
import json

url = "http://127.0.0.1:8000/preopen"

load_dotenv()

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

Base = declarative_base()

class preOpen(Base):
    __tablename__ = "preopen_data"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True, nullable=False)
    last_price = Column(Float)
    change = Column(Float)
    pchange = Column(Float)
    previous_close = Column(Float)  
    final_quantity = Column(Float) 
    timestamp = Column(DateTime, default=datetime.now)

def fetch_data(url):
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data {e}")
        return None

def main():
    engine = create_engine(f"postgresql+psycopg2://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}", echo=True)
    
    Base.metadata.create_all(engine)
        
    Session = sessionmaker(bind=engine)
    session = Session()

    stock_data = fetch_data(url)

    if stock_data:
        for item in stock_data["data"]:
            meta = item["metadata"]
            preopen_entry = preOpen(
                symbol=meta["symbol"],
                last_price=meta.get("lastPrice"),
                change=meta.get("change"),
                pchange=meta.get("pChange"),
                previous_close=meta.get("previousClose"),
                final_quantity=meta.get("finalQuantity"),
            )
            session.add(preopen_entry)

        session.commit()
    engine.dispose()

if __name__ == "__main__":
    main()