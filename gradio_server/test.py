from PIL import Image
from api import *

image = Image.open('orange1.jpeg')

print(run_freshness(image))
print(run_count_vith(image))
print(run_ocr(image))