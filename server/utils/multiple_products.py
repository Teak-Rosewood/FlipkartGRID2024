from db.database import get_sql_db, save_record
from db.models import ImageDatabase, ProductDatabase, ScanDatabase, FreshDatabase

from utils.gradio_clients import perform_ocr, get_freshness 
from utils.gpt import get_gpt_formatted_text, get_estimated_shelf_life, get_pixtral_response

import cv2
import json


def save_cropped_image(image_path, scan_id, image_id, bounding_box):
    image = cv2.imread(image_path)
    x1, y1, x2, y2 = map(int, bounding_box)  # Ensure coordinates are integers
    cropped_image = image[y1:y2, x1:x2]  # Crop the image using the correct format
    cv2.imwrite(f"images/{scan_id}_{image_id}.jpg", cropped_image)
    
def process_fruit(values):
    image_id = 1
    if len(values) == 2:
        scan_id, db = values
    else:
        scan_id, image_id, db = values
    freshness = get_freshness('images/' + scan_id + '_' + str(image_id) + '.jpg')
    if isinstance(freshness, str):
        freshness = json.loads(freshness)
    shelf_life = get_estimated_shelf_life(freshness['type'], freshness['freshness'])
    try:
        shelf_life['days'] = int(shelf_life['days']) 
    except ValueError:
        shelf_life['days'] = None
    fruit_record = FreshDatabase(
        scan_id=scan_id,
        product_id=image_id,
        produce=freshness['type'],
        freshness=float(freshness['freshness']),
        shelf_life=shelf_life['days'],
        summary=shelf_life['summary']
    )
    if len(values) == 2:
        record = db.query(ScanDatabase).filter(ScanDatabase.scan_id == scan_id).first()
        record.processed = True
        db.commit()
        db.refresh(record)
    save_record(fruit_record)

def cropped_image_ocr(values):
    scan_id, image_id, db = values
    image_path = f"images/{scan_id}_{image_id}.jpg"
    ocr_text = None
    image_record = ImageDatabase(
        scan_id=scan_id,
        image_id=image_id,
        ocr_text=ocr_text
    )
    save_record(image_record)
    formated_data = get_pixtral_response(image_path)
    brand_product =formated_data.get("brand_product", "NA"),
    expiry_date = formated_data.get("expiry_date", "NA"),
    expired = formated_data.get("expired", "NA"),
    shelf_life = formated_data.get("shelf_life", "NA"),
    summary = formated_data.get("summary", "NA")

    if isinstance(brand_product, tuple):
        brand_product = brand_product[0]
    if isinstance(expiry_date, tuple):
        expiry_date = expiry_date[0]
    if isinstance(expired, tuple):
        expired = expired[0]
    if isinstance(shelf_life, tuple):
        shelf_life = shelf_life[0]
    if isinstance(summary, tuple):
        summary = summary[0]
        
    # Convert shelf_life to int if it is not "NA"
    try:
        shelf_life = int(shelf_life) if shelf_life != "NA" else None
    except ValueError:
        shelf_life = None
        
    record = ProductDatabase(
        scan_id=scan_id,
        product_id=image_id,
        brand = brand_product,
        expiry_date = expiry_date,
        expired = expired,
        shelf_life = shelf_life,
        summary = summary
    )
    save_record(record)
        
def process_multiple_products(data):
    scan_id, count, classes, bounding_boxes, db = data
    if count > 6:
        count = 6
    for i in range(0, count):
        save_cropped_image(f"images/{scan_id}_1.jpg", scan_id, i+2, bounding_boxes[i])
        
        if classes[i] == "fruit":
            process_fruit((scan_id, i+2, db))
        else:
            cropped_image_ocr((scan_id, i+2, db))
    scan_record = db.query(ScanDatabase).filter(ScanDatabase.scan_id == scan_id).first()
    if scan_record:
        scan_record.processed = True
    db.commit()
