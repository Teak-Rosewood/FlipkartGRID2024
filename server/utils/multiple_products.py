from db.database import get_sql_db, save_record
from db.models import ImageDatabase, ProductDatabase, ScanDatabase, FreshDatabase

from gradio_clients import perform_ocr, get_freshness 
from utils.gpt import get_gpt_formatted_text, get_estimated_shelf_life

import cv2

def save_cropped_image (image_path, scan_id, image_id, bounding_box):
    image = cv2.imread(image_path)
    y1, x1, y2, x2 = bounding_box
    cropped_image = image[x1:x2, y1:y2]
    cv2.imwrite(f"images/{scan_id}_{image_id}.jpg", cropped_image)
    
def process_multiple_products(data):
    scan_id, count, classes, bounding_boxes = data
    for i in range(0, count):
        save_cropped_image(f"images/{scan_id}_1.jpg", scan_id, i+2, bounding_boxes[i])
        
        if classes[i] == "fruit":
            freshness = get_freshness(f"images/{scan_id}_{i+2}.jpg") 
            record = FreshDatabase(
                scan_id=scan_id,
                product_id=i+2,
                produce=classes[i],
                freshness=freshness,
                shelf_life=get_estimated_shelf_life(classes[i], freshness)
            ) 

        else:
            ocr_text = perform_ocr(f"images/{scan_id}_{i+2}.jpg")
            image_record = ImageDatabase(
                scan_id=scan_id,
                image_id=i+2,
                ocr_text=ocr_text
            )
            save_record(image_record)
            formated_data = get_gpt_formatted_text(ocr_text)

            record = ProductDatabase(
                scan_id=scan_id,
                product_id=i+2,
                brand=formated_data.get("brand_product", "NA"),
                expiry_date=formated_data.get("expiry_date", "NA"),
                expired=formated_data.get("expired", "NA"),
                shelf_life=formated_data.get("shelf_life", "NA"),
                summary=formated_data.get("summary", "NA")
            )
        save_record(record)
    db = get_sql_db()
    try:
        scan_record = db.session.query(ScanDatabase).filter(ScanDatabase.scan_id == scan_id).first()
        if scan_record:
            scan_record.processed = True
            db.session.add(scan_record)
        db.session.commit()
    finally:
        db.session.close()
     