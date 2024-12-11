from db.database import get_sql_db, save_record
from db.models import ImageDatabase, ProductDatabase, ScanDatabase

from gradio_clients import perform_ocr
from utils.gpt import get_gpt_formatted_text

def single_image_ocr(scan_id):
    db = get_sql_db()
    try:
        records = db.session.query(ImageDatabase).filter(ImageDatabase.scan_id == scan_id).all()
        ocr_texts = ""
        for i, record in enumerate(records):
            image_path = f"images/{record.scan_id}_{record.image_id}.jpg"
            ocr_text = perform_ocr(image_path)
            ocr_texts += "image " + str(i+1) + ": " + record.ocr_text + "\n"
            record.ocr_text = ocr_text
        data = get_gpt_formatted_text(ocr_texts)
    
        brand_product = data.get("brand_product", "NA")
        expiry_date = data.get("expiry_date", "NA")
        expired = data.get("expired", "NA")
        shelf_life = data.get("shelf_life", "NA")
        summary = data.get("summary", "NA")

        record = ProductDatabase (
            scan_id = scan_id,
            product_id = 1,
            brand = brand_product,
            expiry_date = expiry_date,
            expired = expired,
            shelf_life = shelf_life,
            summary = summary
        )
        scan_record = db.session.query(ScanDatabase).filter(ScanDatabase.scan_id == scan_id).first()
        if scan_record:
            scan_record.processed = True
            db.session.add(scan_record)
        save_record(record)

        db.session.commit()
    finally:
        db.session.close()

    
