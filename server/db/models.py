from sqlalchemy import Column, Integer, Float,  String, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    other_data = Column(JSON)
    price = Column(Float)
    shelf_life = Column(Integer)
    total_no = Column(Integer)

class ProductTransaction(Base):
    __tablename__ = "product_transactions"
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey(Product.item_id))
    no = Column(Integer)
    total_price = Column(Float)
    shelf_life_remaining = Column(Integer)

class FruitsVegetables(Base): 
    __tablename__ = "fruits_vegetables"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    shelf_life = Column(Integer, index=True)
    

    