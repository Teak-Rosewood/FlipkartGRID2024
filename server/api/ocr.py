from fastapi import FastAPI, Request
from io import BytesIO
import logging
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import numpy as np
import cv2
from symspellpy.symspellpy import SymSpell, Verbosity
import pkg_resources
import re
import uvicorn

def correct_text(text):
    if re.search(r'\d', text):
        return text
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term
    return text

logging.getLogger().setLevel(logging.ERROR)

ocr = PaddleOCR(use_angle_cls=True, lang="en")

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

app = FastAPI()

@app.post("/ocr/")
async def process_image(request: Request):
    global ocr
    raw_image = await request.body()
    image = Image.open(BytesIO(raw_image))
    image = np.array(image)[:, :, ::-1].copy()

    result = ocr.ocr(image)[0]
    txts = [line[1][0] for line in result]
    extracted_text = [correct_text(text) for text in txts]

    return {"extracted_text": extracted_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)