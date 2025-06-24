# app/main.py
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# Подключение к БД
DATABASE_URL = "postgresql://myappuser:secretpassword@192.168.1.126/myappdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Модель таблицы
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    db = SessionLocal()
    items = db.query(Item).all()
    return {"items": [item.name for item in items]}

@app.post("/add/{name}")
def add_item(name: str):
    db = SessionLocal()
    item = Item(name=name)
    db.add(item)
    db.commit()
    return {"message": f"Added {name}"}

