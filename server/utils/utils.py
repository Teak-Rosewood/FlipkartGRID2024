from pydantic import BaseModel
import uuid

class ImageData(BaseModel):
    images: list[str]

def get_uuid():
    return str(uuid.uuid4())