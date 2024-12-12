from pydantic import BaseModel
import uuid

class ImageData(BaseModel):
    images: list[str]

def get_uuid():
    return str(uuid.uuid4())

class ImageDataPlusID(BaseModel):
    images: list[str]
    scan_id: str