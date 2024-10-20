import logging 
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np
import cv2
from symspellpy.symspellpy import SymSpell, Verbosity
import pkg_resources
import re

# Initialize logging
logging.getLogger().setLevel(logging.ERROR)

# Initialize OCR model
ocr = PaddleOCR(use_angle_cls=True, lang="en") 

 # Initialize SymSpell for spell correction
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Load dictionary (frequency words list)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

def correct_text(text):

    # Skip correction if the text contains numbers
    if re.search(r'\d', text):
        return text
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term
    return text

def get_ocr_text(img_path):
    result = ocr.ocr(img_path, cls=True)
    result = result[0]
    txts = [line[1][0] for line in result]

    # Perform spell correction and spacing, ignoring text with numbers
    corrected_texts = [correct_text(text) for text in txts]

    final_text = " ".join(corrected_texts)
    return final_text