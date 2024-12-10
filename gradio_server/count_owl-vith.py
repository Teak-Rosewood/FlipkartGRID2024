import gradio as gr
from transformers import pipeline
import numpy as np
from PIL import Image, ImageDraw
import time
import json


# Initialize the detector pipeline before hand
checkpoint = "google/owlv2-base-patch16-ensemble"
detector = pipeline(model=checkpoint, task="zero-shot-object-detection", device=0)
candidate_labels = ["fruit", "vegetable", "grocery", "bottle", "package"]

def detect_objects(image, min_score=0.2, max_area=400*400, candidate_labels=None):
    # Use default candidate labels if none provided
    if candidate_labels is None:
        candidate_labels = ["fruit", "vegetable", "grocery", "bottle", "package"]

    # Get original image dimensions
    original_width, original_height = image.size
    original_area = original_width * original_height

    # If the current area exceeds the maximum area, resize the image
    if original_area > max_area:
        scale_factor = (max_area / original_area) ** 0.5
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        image = image.resize((new_width, new_height))
    else:
        new_width, new_height = original_width, original_height

    # Run the object detection model
    start = time.time()
    predictions = detector(image, candidate_labels=candidate_labels)
    end = time.time()
    print("Time taken for detection:", round(end-start, 2), "seconds")

    # Store boxes, labels, and scores
    boxes = []
    labels = []
    scores = []

    # Extract information for statistical analysis and filter out low-confidence predictions
    for prediction in predictions:
        box = prediction["box"]
        label = prediction["label"]
        score = prediction["score"]

        if score < min_score:
            continue

        boxes.append(box)
        labels.append(label)
        scores.append(score)

    # Convert scores to a numpy array for statistical processing
    scores = np.array(scores)

    # Perform IQR-based outlier removal
    Q1 = np.percentile(scores, 25)
    Q3 = np.percentile(scores, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR

    # Filter out predictions with scores lower than the lower bound
    filtered_boxes = [box for box, score in zip(boxes, scores) if score >= lower_bound]
    filtered_labels = [label for label, score in zip(labels, scores) if score >= lower_bound]
    filtered_scores = [score for score in scores if score >= lower_bound]

    output = {}
    output['count'] = str(len(filtered_boxes))
    output['class'] = filtered_labels
    output['box'] = filtered_boxes
    output['score'] = filtered_scores
    
    json_output = json.dumps(output)
    # Return the number of objects detected along with the modified image
    return str(json_output)

# Gradio interface function
def gradio_interface(image):
    output = detect_objects(image)
    return output

# Define Gradio input and output components
image_input = gr.Image(type="pil")

# Create the Gradio interface
demo = gr.Interface(
    fn=gradio_interface,
    inputs=image_input,
    outputs='text',
    title="Object Detection with OWL-ViT",
    description="Upload an image, and the model will detect objects and return the number of objects along with the image showing the bounding boxes."
)

demo.launch(share=False)