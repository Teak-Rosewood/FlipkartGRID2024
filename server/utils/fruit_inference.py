from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import cv2

# Load the image processor and model
processor = AutoImageProcessor.from_pretrained("hgarg/fruits")
model = AutoModelForImageClassification.from_pretrained("hgarg/fruits")

def detect_fruit(image):
    global processor,model
    color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    image = Image.fromarray(color_coverted) 
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    predictions = outputs.logits.argmax(-1)
    predicted_class = model.config.id2label[predictions.item()]
    return predicted_class