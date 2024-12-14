from sqlalchemy import Column, Integer, Boolean, Float, String, JSON, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class ScanDatabase(Base):
    __tablename__ = "scan_db"
    scan_id = Column(String, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.now())
    count = Column(Integer)
    processed = Column(Boolean, default=False)
    items_detected = Column(JSON)
    '''
    items_detected = {
        classes : [class1, class2, class3],
        bounding_box : [[x1, y1, x2, y2], [x1, y1, x2, y2], [x1, y1, x2, y2]]
        scores : [score1, score2, score3]
    '''
    item_summary = Column(JSON)

class ImageDatabase(Base):
    __tablename__ = "image_db"
    image_id  = Column(Integer, primary_key=True)
    scan_id = Column(String, ForeignKey(ScanDatabase.scan_id, ondelete='CASCADE'), primary_key=True)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.now())
    ocr_text = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint('image_id', 'scan_id', name='iamge_db_pk'),
    )

class ProductDatabase(Base): 
    __tablename__ = "product_db"
    product_id  = Column(Integer, primary_key=True)
    scan_id = Column(String, ForeignKey(ScanDatabase.scan_id, ondelete='CASCADE'), primary_key=True)
    brand = Column(String)
    price = Column(String)
    expiry_date = Column(String)
    expired = Column(String)
    shelf_life = Column(Integer, index=True)
    summary = Column(String)

class FreshDatabase(Base):
    __tablename__ = "fres_db"
    product_id  = Column(Integer, primary_key=True)
    scan_id = Column(String, ForeignKey(ScanDatabase.scan_id, ondelete='CASCADE'), primary_key=True)
    produce = Column(String)
    freshness = Column(Float)
    shelf_life = Column(Integer, index=True)
    summary = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'scan_id', name='fesh_db_pk'),
    )
    

    