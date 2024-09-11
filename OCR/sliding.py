import logging
from paddleocr import PaddleOCR
import cv2
from symspellpy.symspellpy import SymSpell, Verbosity
import pkg_resources
import re
import numpy as np

# Set logging level to ERROR to suppress debug/info messages
logging.getLogger().setLevel(logging.ERROR)

# Initialize OCR model with text detection
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)

# Detect text regions and extract bounding boxes
img_path = 'images/soy.jpeg'
result = ocr.ocr(img_path, det=True)  # Use det=True for text detection

# Load the image
image = cv2.imread(img_path)

# Get the image dimensions (height and width)
img_height, img_width = image.shape[:2]

arr = []

# Function to apply preprocessing (Sharpening without Grayscaling)
def preprocess_image(cropped_image):
    # Sharpen the color image using a kernel
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Sharpening kernel
    sharpened_image = cv2.filter2D(cropped_image, -1, kernel)

    return sharpened_image

# Crop the text regions and apply OCR only to those areas
for region in result[0]:  # result[0] contains bounding boxes
    box = region[0]  # Get the coordinates of the text box
    x_min = int(max(min([point[0] for point in box]), 0))  # Ensure within bounds
    y_min = int(max(min([point[1] for point in box]), 0))  # Ensure within bounds
    x_max = int(min(max([point[0] for point in box]), img_width))  # Ensure within bounds
    y_max = int(min(max([point[1] for point in box]), img_height))  # Ensure within bounds

    # Crop the image to the text region
    cropped_image = image[y_min:y_max, x_min:x_max]
    
    if cropped_image.size == 0:
        continue  # Skip empty cropped regions

    # Preprocess the cropped image (apply sharpening without grayscaling)
    preprocessed_image = preprocess_image(cropped_image)

    # Apply OCR to the preprocessed region
    text_result = ocr.ocr(preprocessed_image)
    
    if text_result and len(text_result) > 0 and text_result[0]:  # Ensure text_result is valid
        # Extract and store the recognized text
        for line in text_result[0]:  # text_result[0] contains recognized lines
            if len(line) > 1:
                arr.append(line[1][0])  # line[1][0] contains the recognized text

# Initialize SymSpell for spell correction
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Load dictionary (frequency words list)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# Function to perform spell correction
def correct_text(text):
    # Skip correction if the text contains numbers
    if re.search(r'\d', text):
        return text
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term
    return text

# Perform spell correction and spacing, ignoring text with numbers
corrected_texts = [correct_text(text) for text in arr]

# Print corrected text
for line in corrected_texts:
    print(line)
