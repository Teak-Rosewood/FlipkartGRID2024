# Flipkart GRID 6.0 Robotics drive - Brief Submission & Presentation Round

## Client

To build client run

```
npm i
npm run dev
```

## Server

To build server run

```
docker compose up
```

## Model hosting

Gradio is used to host the models locally
Requires Python 3.10+, tested on Python 3.11 with CUDA 12.7

```bash
pip install -r requirements.txt
```

```bash
python run.py
```
To import API

```
from api import run_count_vith,run_freshness,run_ocr
```

## Pipeline
3 Models: 
Grounding DINO: Zero Shot Object detection
Custom ResNet50: Fruit/Vegetable classification and freshnesh detection
EasyOCR: Optical Character Recognition

Grounding DINO detects and classifies objects based on pre set labels (fruit, vegetables, bottles, containers etc.).
Each detection is cropped and sent to 
1) Fruit/Vegetable classification and and freshnesh detection if fruit or vegetable is detected.
2) EasyOCR else. Output of Easy OCR is passed through spell check for refining.
Outputs are combined and passed through Mistral model for processing and refactoring.

Client is made on ReactJS.
Server is made on FastAPI
Databasing on Postgres SQL.
