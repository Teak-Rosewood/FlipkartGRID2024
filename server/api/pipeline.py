from fastapi import APIRouter, Form, BackgroundTasks, HTTPException
import json

from db.models import ScanDatabase, ImageDatabase, ProductDatabase, FreshDatabase
from db.database import save_record, get_sql_db

from utils.utils import ImageData, get_uuid
from utils.ocr import single_image_ocr
from utils.multiple_products import process_multiple_products
from utils.image_functions import store_image
from utils.gradio_clients import detect_objects

router = APIRouter()

@router.get('/')
async def root():
    return {"message": "this is the pipeline router"}

@router.post("/initial_image_info")
def root(multiple_products: BackgroundTasks, data: ImageData):
    scan_id = get_uuid()
    store_image(data.images[0], scan_id)
    count, classes, bounding_boxes, scores = detect_objects('images/' + scan_id + '_1.jpg')

    record = ScanDatabase(
        scan_id=scan_id,
        count=count,
        items_detected= {
            "classes": classes,
            "bounding_boxes": bounding_boxes,
            "scores": scores
        }
    )
    if count == 1 and classes[0] != "fruit":
        image_record = ImageDatabase(
            scan_id=scan_id,
            image_id=1,
        )
        save_record(image_record)
    values = scan_id, count, classes, bounding_boxes
    
    if count > 1:
        multiple_products.add_task(process_multiple_products, values)
        

    save_record(record)

    return {
        "count": count,
        "scan_id": scan_id,
        "classes": classes,
        "bounding_boxes": bounding_boxes,
        "scores": scores
    }

@router.post("/single_image_info")
def root(image_ocr_process: BackgroundTasks, data: ImageData, scan_id: str):
    for i, image in enumerate(data.images):
        store_image(image, scan_id, i+2, inDB=True)
    image_ocr_process.add_task(single_image_ocr, scan_id)
    return {"message": "Image Processing"}

@router.post("/multiple_image_info")
def root(image_ocr_process: BackgroundTasks, data: ImageData, scan_id: str):
    for i, image in enumerate(data.images):
        store_image(image, scan_id, i+2, inDB=True)
    return {"message": "Image Processing"}

@router.get("/image_info/{scan_id}")
def get_image_info(scan_id: str):
    db = get_sql_db()
    try:
        product_scan_record = db.session.query(ScanDatabase).filter(ScanDatabase.scan_id == scan_id).first()
        if not product_scan_record:
            raise HTTPException(status_code=404, detail="Scan ID not found")
        
        if product_scan_record.processed:
            product_data = db.session.query(ProductDatabase).filter(ProductDatabase.scan_id == scan_id).all()
            fresh_data = db.session.query(FreshDatabase).filter(FreshDatabase.scan_id == scan_id).all()
            
            return {
                "product_data": [record.__dict__ for record in product_data],
                "fresh_data": [record.__dict__ for record in fresh_data]
            }
        else:
            return {"message": "Scan is not yet processed"}
    finally:
        db.session.close()
