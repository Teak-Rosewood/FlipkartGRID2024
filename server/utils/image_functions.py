import io
import base64
import numpy as np
import cv2

from db.database import save_record
from db.models import ImageDatabase

from PIL import Image

def store_image(base64_image: str, scan_id: str, image_id: int, inDB = False) -> bool:
    image_data = base64_image.split(",")[1]
    image_bytes = io.BytesIO(base64.b64decode(image_data))

    image = Image.open(image_bytes).convert("RGB")
    image.save(f"images/{scan_id}_{image_id}.jpg")

    if inDB:
        image_record = ImageDatabase(
            scan_id=scan_id,
            image_id=image_id,
        )
        save_record(image_record)

    return True

def read_image_from_base64(base64_image: str) -> np.ndarray:
    image_data = base64_image.split(",")[1]
    image_bytes = io.BytesIO(base64.b64decode(image_data))

    image = Image.open(image_bytes).convert("RGB")

    image_array = np.array(image)

    image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    return image_array