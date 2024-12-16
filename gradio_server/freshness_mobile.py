import torch
from PIL import Image
import os
import time
from transformers import AutoProcessor, AutoModelForVisualQuestionAnswering
from torchvision import models
import torch.nn as nn
import torch
import json
from torchvision import transforms
import gradio as gr


transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to the model's input size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize as in ImageNet
])

# Define the model architecture
mob_model = models.mobilenet_v2(pretrained=False)
mob_model.classifier[1] = nn.Linear(mob_model.last_channel, 2)
mob_model.load_state_dict(torch.load("models/mobilenet_freshness_model.pth"))
mob_model.to('cuda')
mob_model.eval()

processor = AutoProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = AutoModelForVisualQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
model.eval()
model.to('cuda')  # Send the model to GPU

def get_answer_from_image(img):
    # start = time.time()
    prompt = "Question: What fruit or vegetable is present? Answer:"
    inputs = processor(img, text=prompt, return_tensors="pt").to('cuda', torch.float16)

    # Generate text
    generated_ids = model.generate(**inputs, max_new_tokens=10)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    # print(f"Processing time: {time.time() - start:.2f} seconds")
    return generated_text

def freshness_run(image):
    input_tensor = transform(image).unsqueeze(0).to('cuda')
    prediction = None
    with torch.no_grad():  # Disable gradient computation
        output = mob_model(input_tensor)
        prediction = torch.sigmoid(output)
    # print(prediction)
    return float(torch.max(prediction))

def run_classify_and_freshness(image):
    output = {}
    output['type'] = get_answer_from_image(image)
    output['freshness'] = freshness_run(image)

    json_output = json.dumps(output)
    return str(json_output)

# Define Gradio input and output components
image_input = gr.Image(type="pil")

# Create the Gradio interface
demo = gr.Interface(
    fn=run_classify_and_freshness,
    inputs=image_input,
    outputs='text',
    title="Frshness prediction",
    description="Upload an image, and the model will detect objects and return the number of objects along with the image showing the bounding boxes."
)

demo.launch(share=True)