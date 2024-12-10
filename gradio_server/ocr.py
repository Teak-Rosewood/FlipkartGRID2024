import easyocr
from PIL import Image, ImageEnhance
import re
from symspellpy.symspellpy import SymSpell
import torch
import gradio as gr
import pkg_resources
import json

# Initialize OCR model
ocr = easyocr.Reader(['en'], gpu=True)  # Use GPU if available

# Initialize SymSpell for spell correction
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

def preprocess_and_run_ocr(image):
    
    img = image.convert('L')  # Convert to grayscale
    img = ImageEnhance.Contrast(img).enhance(2.0)  # Increase contrast
    img = ImageEnhance.Sharpness(img).enhance(2.0)  # Increase sharpness

    # Save the preprocessed image temporarily (if required by OCR)
    preprocessed_img = 'preprocessed_image.jpg'
    img.save(preprocessed_img)

    # Perform OCR using easyOCR
    result = ocr.readtext(preprocessed_img)

    # Extract text from OCR result
    txts = [text[1] for text in result]

    # Spell correction function
    def correct_text(text):
        # Skip correction if the text contains numbers
        if re.search(r'\d', text):
            return text
        suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
        if suggestions:
            return suggestions[0].term
        return text

    # Perform spell correction and spacing, ignoring text with numbers
    corrected_texts = [correct_text(text) for text in txts]
    text = {}
    text['text'] = corrected_texts
    json_output = json.dumps(text)
    # Return concatenated corrected text
    return str(json_output)


# Define Gradio input and output components
image_input = gr.Image(type="pil")

# Create the Gradio interface
demo = gr.Interface(
    fn=preprocess_and_run_ocr,
    inputs=image_input,
    outputs='text',
    title="Frshness prediction",
    description="Upload an image, and the model will detect objects and return the number of objects along with the image showing the bounding boxes."
)

demo.launch(share=False)