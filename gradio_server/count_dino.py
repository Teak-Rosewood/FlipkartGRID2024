import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
import time
import numpy as np
import json
import torch
import gradio as gr

# Model setup
model_id = "IDEA-Research/grounding-dino-tiny"
device = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device)
text="Container. Bottle. Fruit. Vegetable. Packet."
iou_threshold=0.4
box_threshold=0.3
score_threshold=0.4

# Function to detect objects in an image and return a JSON with count, class, box, and score
def detect_objects(image):

    # Prepare inputs for the model
    inputs = processor(images=image, text=text, return_tensors="pt").to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Post-process results
    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        box_threshold=box_threshold,
        text_threshold=score_threshold,
        target_sizes=[image.size[::-1]]
    )

    # Function to calculate IoU (Intersection over Union)
    def iou(box1, box2):
        x1, y1, x2, y2 = box1
        x1_2, y1_2, x2_2, y2_2 = box2

        # Calculate intersection area
        inter_x1 = max(x1, x1_2)
        inter_y1 = max(y1, y1_2)
        inter_x2 = min(x2, x2_2)
        inter_y2 = min(y2, y2_2)

        if inter_x2 < inter_x1 or inter_y2 < inter_y1:
            return 0.0  # No intersection

        intersection_area = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)

        # Calculate union area
        area1 = (x2 - x1) * (y2 - y1)
        area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = area1 + area2 - intersection_area

        return intersection_area / union_area

    # Filter out overlapping boxes using NMS (Non-Maximum Suppression)
    filtered_boxes = []
    filtered_labels = []
    filtered_scores = []

    for i, (box, label, score) in enumerate(zip(results[0]['boxes'], results[0]['labels'], results[0]['scores'])):
        keep = True
        for j, (box2, label2, score2) in enumerate(zip(filtered_boxes, filtered_labels, filtered_scores)):
            # If IoU is above the threshold, discard the box
            if iou(box.tolist(), box2) > iou_threshold:
                keep = False
                break
        if keep:
            filtered_boxes.append(box.tolist())
            filtered_labels.append(label)
            filtered_scores.append(score.item())

    # Prepare the output in the requested format
    output = {
        "count": len(filtered_boxes),
        "class": filtered_labels,
        "box": filtered_boxes,
        "score": filtered_scores
    }

    return json.dumps(output)

# Define Gradio input and output components
image_input = gr.Image(type="pil")

# Create the Gradio interface
demo = gr.Interface(
    fn=detect_objects,
    inputs=image_input,
    outputs='text',
    title="Frshness prediction",
    description="Upload an image, and the model will detect objects and return the number of objects along with the image showing the bounding boxes."
)

demo.launch(share=False)
