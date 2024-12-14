from fastapi import APIRouter, Form, BackgroundTasks, HTTPException, Depends
import json

from db.models import ScanDatabase, ImageDatabase, ProductDatabase, FreshDatabase
from db.database import save_record, get_sql_db

from sqlalchemy.orm import Session 

from utils.utils import ImageData,ImageDataPlusID, get_uuid
from utils.ocr import single_image_ocr
from utils.multiple_products import process_multiple_products, process_fruit
from utils.image_functions import store_image
from utils.gradio_clients import detect_objects, get_freshness
from utils.gpt import get_estimated_shelf_life

router = APIRouter()

@router.get('/')
async def root():
    return {"message": "this is the pipeline router"}

@router.post("/initial_image_info")
def root(multiple_products: BackgroundTasks, data: ImageData, db: Session = Depends(get_sql_db)):
    scan_id = get_uuid()
    store_image(data.images[0], scan_id, 1)
    
    count, classes, bounding_boxes, scores = detect_objects('images/' + scan_id + '_1.jpg')
    print("classes", classes)
    record = ScanDatabase(
        scan_id=scan_id,
        count=count,
        items_detected= {
            "classes": classes,
            "bounding_boxes": bounding_boxes,
            "scores": scores
        }
    )
    
    save_record(record)
    
    if count == 1 and classes[0] != "fruit":
        image_record = ImageDatabase(
            scan_id=scan_id,
            image_id=1,
        )
        save_record(image_record)
    values = scan_id, count, classes, bounding_boxes, db
    
    if count == 1 and classes[0] == "fruit":
        values = scan_id, db
        multiple_products.add_task(process_fruit, values)
         
    if count > 1:
        multiple_products.add_task(process_multiple_products, values)

    return {
        "count": count,
        "scan_id": scan_id,
        "classes": classes,
        "bounding_boxes": bounding_boxes,
        "scores": scores
    }

@router.post("/single_image_info")
def root(image_ocr_process: BackgroundTasks, data: ImageDataPlusID, db: Session = Depends(get_sql_db)):
    for i, image in enumerate(data.images):
        store_image(image, data.scan_id, i+2, inDB=True)
    image_ocr_process.add_task(single_image_ocr, data.scan_id, db)
    return {"message": "Image Processing"}

@router.get("/image_info/{scan_id}")
def get_image_info(scan_id: str, db: Session = Depends(get_sql_db)):
    product_scan_record = db.query(ScanDatabase).filter(ScanDatabase.scan_id == scan_id).first()
    if not product_scan_record:
        raise HTTPException(status_code=404, detail="Scan ID not found")
    
    if product_scan_record.processed:
        product_data = db.query(ProductDatabase).filter(ProductDatabase.scan_id == scan_id).all()
        fresh_data = db.query(FreshDatabase).filter(FreshDatabase.scan_id == scan_id).all()
        
        return {
            "product_data": [record.__dict__ for record in product_data],
            "fresh_data": [record.__dict__ for record in fresh_data]
        }
    else:
        print("not processed")
        return {"message": "Scan is not yet processed"}

@router.get("/all_data")
def root(db: Session = Depends(get_sql_db)):
    product_data = db.query(ProductDatabase).all()
    fresh_data = db.query(FreshDatabase).all()
    scan_data = db.query(ScanDatabase).all()
    image_data = db.query(ImageDatabase).all()
    return {
        "product_data": [record.__dict__ for record in product_data],
        "fresh_data": [record.__dict__ for record in fresh_data],
        "image_data": [record.__dict__ for record in image_data],
        "scan_data": [record.__dict__ for record in scan_data]
    }
