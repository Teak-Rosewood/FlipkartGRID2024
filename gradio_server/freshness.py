import torch
import joblib
from torchvision import transforms
from PIL import Image
from models.freshness_model import MultiOutputModel
import torch.nn.functional as F  # For applying sigmoid
import gradio as gr
import json

# Define the paths
MODEL_PATH = 'models/multi_output_model.pth'
LABEL_ENCODER_TYPE_PATH = 'models/label_encoder_type.pkl'

# Load the label encoder
label_encoder_type = joblib.load(LABEL_ENCODER_TYPE_PATH)

# Load the model
model = MultiOutputModel(num_classes_type=len(label_encoder_type.classes_))
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()  # Set the model to evaluation mode

# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to match the input size of the model
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize using ImageNet stats
])

def preprocess_image(image: Image.Image):
    """Preprocess the input image."""
    return transform(image).unsqueeze(0)  # Add batch dimension

def run_inference(image: Image.Image):
    """Run inference on a single image."""
    # Preprocess the image
    input_tensor = preprocess_image(image)
    
    # Move to device (GPU if available)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    input_tensor = input_tensor.to(device)
    
    # Forward pass
    with torch.no_grad():
        type_output, freshness_output = model(input_tensor)
    
    # Apply sigmoid to freshness output (to get probability)
    freshness_output = torch.sigmoid(freshness_output.squeeze())  # Sigmoid for binary classification
    
    # Decode predictions
    _, predicted_type_idx = torch.max(type_output, 1)
    predicted_type = label_encoder_type.inverse_transform([predicted_type_idx.item()])
    
    output = {}
    output['type'] = str(predicted_type[0])
    output['freshness'] = str(float(freshness_output.item()))

    json_output = json.dumps(output)
    return str(json_output)


# Define Gradio input and output components
image_input = gr.Image(type="pil")

# Create the Gradio interface
demo = gr.Interface(
    fn=run_inference,
    inputs=image_input,
    outputs='text',
    title="Frshness prediction",
    description="Upload an image, and the model will detect objects and return the number of objects along with the image showing the bounding boxes."
)

demo.launch(share=True)