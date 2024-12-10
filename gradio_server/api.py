from gradio_client import Client, handle_file
from PIL import Image
import json
import io
import os
import time

data = None

with open('metadata.json', 'r') as file:
    data = json.load(file)

vith_link = data['vith_link']
freshness_link = data['freshness_link']
ocr_link = data['ocr_link']

vith_working = True
freshness_working = True
ocr_working = True

client_vith = None
client_freshness = None
client_ocr = None

try:
    client_vith = Client(vith_link)
except Exception as e:
    print("Failed to load vith model")
    vith_working = False

try:
    client_freshness = Client(freshness_link)
except Exception as e:
    print("Failed to load freshness model")
    freshness_working = False

try:
    client_ocr = Client(ocr_link)
except Exception as e:
    print("Failed to load ocr model")
    ocr_working = False


def run_count_vith(image: Image):
    filename = f"temp/temp_{os.getpid()}_{int(time.time())}.jpg"
    image.save(filename)
    output = client_vith.predict(image=handle_file(filename),api_name='/predict') if vith_working else None
    os.remove(filename)
    return output

def run_freshness(image: Image):
    filename = f"temp/temp_{os.getpid()}_{int(time.time())}.jpg"
    image.save(filename)
    output = client_freshness.predict(image=handle_file(filename),api_name='/predict') if freshness_working else None
    os.remove(filename)
    return output

def run_ocr(image: Image):
    filename = f"temp/temp_{os.getpid()}_{int(time.time())}.jpg"
    image.save(filename)
    output = client_ocr.predict(image=handle_file(filename),api_name='/predict') if ocr_working else None
    os.remove(filename)
    return output