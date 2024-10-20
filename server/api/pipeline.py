from fastapi import APIRouter, Form
from pydantic import BaseModel
import base64
import cv2
import io
from PIL import Image
import numpy as np
from utils.obj_detection import detect_objects
from utils.ocr_detection import get_ocr_text
from utils.gpt import get_gpt_formatted_text 

router = APIRouter()

class ImageData(BaseModel):
    image1: str
    # image2: str
ip_camera_url = 'http://192.168.1.6:8080/video'
cap2 = cv2.VideoCapture(ip_camera_url)
@router.get('/')
async def root():
    return {"message": "this is the pipeline router"}

def read_image_from_base64(base64_image: str) -> np.ndarray:
    # Decode the base64 image
    image_data = base64_image.split(",")[1]
    image_bytes = io.BytesIO(base64.b64decode(image_data))

    # Open the image using PIL and convert to RGB
    image = Image.open(image_bytes).convert("RGB")

    # Convert PIL image to OpenCV format (numpy array)
    image_array = np.array(image)

    # Convert RGB to BGR, because OpenCV uses BGR format
    image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    return image_array

@router.post("/process_images")
def root(data: ImageData):
    # Convert the received base64 images to OpenCV format
    try:
        image_cv1 = read_image_from_base64(data.image1)
        _, image_cv2 = cap2.read()

    except Exception as e:
        return {"error": f"Failed to convert images: {str(e)}"}
    num, img = detect_objects(image_cv2) 
    if(num >= 0):
        text1 = get_ocr_text(image_cv1)
        text2 = get_ocr_text(image_cv2)
        combined_text = "Frame 1: " + text1 + " Frame 2: " + text2
        print(combined_text)
        formated_text = get_gpt_formatted_text(combined_text)
    else:
        formated_text =  {
        "mfg_date": None,
        "net_weight": None,
        "price": None,
        "productname": None,
        "shelf_life": None
        }   

    # Example response: just return a message indicating success
    return {
        "message": "Processing done",
        "count": 1,
        "product": True,
        "fruit": None,
        "freshness": None,
        "result": formated_text
    }