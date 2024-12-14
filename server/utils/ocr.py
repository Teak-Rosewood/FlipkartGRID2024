from db.database import get_sql_db, save_record
from db.models import ImageDatabase, ProductDatabase, ScanDatabase

from utils.gradio_clients import perform_ocr
from utils.gpt import get_pixtral_response

def single_image_ocr(scan_id, db):
    try:
        records = db.query(ImageDatabase).filter(ImageDatabase.scan_id == scan_id).all()
        ocr_texts = ""
        for i, record in enumerate(records):
            image_path = f"images/{record.scan_id}_{record.image_id}.jpg"
            ocr_text = perform_ocr(image_path)
            ocr_texts += "image " + str(i+1) + ": " + ocr_text + "\n"
            record.ocr_text = ocr_text
        image_path = f"images/{scan_id}_1.jpg"
        formated_data = get_pixtral_response(image_path, ocr_texts)
        brand_product =formated_data.get("brand_product", "NA"),
        price =formated_data.get("price", "NA"),
        expiry_date = formated_data.get("expiry_date", "NA"),
        expired = formated_data.get("expired", "NA"),
        shelf_life = formated_data.get("shelf_life", "NA"),
        summary = formated_data.get("summary", "NA")

        if isinstance(brand_product, tuple):
            brand_product = brand_product[0]
        if isinstance(price, tuple):
            price = price[0]
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
            product_id=1,
            brand = brand_product,
            price = price,
            expiry_date = expiry_date,
            expired = expired,
            shelf_life = shelf_life,
            summary = summary
        )
        save_record(record)
        scan_record = db.query(ScanDatabase).filter(ScanDatabase.scan_id == scan_id).first()
        if scan_record:
            scan_record.processed = True
        db.commit()
    finally:
        db.close()

    
