from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    metadata = Column(JSON)

class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey(Item.item_id))
    number = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.datetime.UTC))

    