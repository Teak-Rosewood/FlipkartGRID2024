from gradio_client import Client, handle_file
import os
import json 

count_working = True
freshness_working = True
ocr_working = True

count_client = None
ocr_client = None
freshness_client = None

try:
    count_client = Client(os.environ['COUNT_CLIENT_URL'])
except Exception as e:
    print("Count client not found")

try:
    ocr_client = Client(os.environ['OCR_CLIENT_URL'])
except Exception as e:
    print("OCR client not found")

try:
    freshness_client = Client(os.environ['FRESHNESS_CLIENT_URL'])
except Exception as e:
    print("Freshness client not found")

def detect_objects(image_path):
    res = count_client.predict(
        image=handle_file(image_path),
        api_name = "/predict"
    ) if count_working else None
    
    predictions = json.loads(res)
    
    count = predictions['count']
    classes = predictions['class']
    bounding_boxes = predictions['box']
    scores = predictions['score']

    return count, classes, bounding_boxes, scores

def perform_ocr(image_path):
    res = ocr_client.predict(
        image=handle_file(image_path),
        api_name = "/predict"
    ) if ocr_working else None
    return res

def get_freshness(image_path):
    res = freshness_client.predict(
        image=handle_file(image_path),
        api_name = "/predict"
    ) if freshness_working else None
    return res



    