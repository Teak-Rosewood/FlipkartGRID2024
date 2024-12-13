# Flipkart GRID 6.0 Robotics drive - Brief Submission & Presentation Round

## Running Web Server - 

[link](https://grid2024.saatwik.in/)

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
pip install -r gradio_server/requirements.txt
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
Website hosted on Amazon EC2

## Database Schema

### **scan_db**
| Column Name      | Data Type     | Constraints                                   |
|------------------|---------------|-----------------------------------------------|
| `scan_id`        | `String`      | Primary Key, Indexed                         |
| `timestamp`      | `TIMESTAMP`   | Default: Current Timestamp                   |
| `count`          | `Integer`     | None                                         |
| `processed`      | `Boolean`     | Default: `False`                             |
| `items_detected` | `JSON`        | None                                         |
| `item_summary`   | `JSON`        | None                                         |

**Notes:**  
`items_detected` contains a nested JSON structure with keys:  
- `classes` (list of class names)  
- `bounding_box` (list of bounding box coordinates)  
- `scores` (list of detection scores)

---

### **image_db**
| Column Name      | Data Type     | Constraints                                   |
|------------------|---------------|-----------------------------------------------|
| `image_id`       | `Integer`     | Primary Key (composite)                      |
| `scan_id`        | `String`      | Foreign Key (references `scan_db.scan_id`), Primary Key (composite) |
| `timestamp`      | `TIMESTAMP`   | Default: Current Timestamp                   |
| `ocr_text`       | `String`      | None                                         |

**Table Constraints:**  
- **Primary Key**: Composite (`image_id`, `scan_id`)  
- **Foreign Key**: `scan_id` references `scan_db(scan_id)` with `ON DELETE CASCADE`

---

### **product_db**
| Column Name      | Data Type     | Constraints                                   |
|------------------|---------------|-----------------------------------------------|
| `product_id`     | `Integer`     | Primary Key                                  |
| `scan_id`        | `String`      | Foreign Key (references `scan_db.scan_id`), Primary Key (composite) |
| `brand`          | `String`      | None                                         |
| `expiry_date`    | `TIMESTAMP`   | None                                         |
| `expired`        | `Boolean`     | None                                         |
| `shelf_life`     | `Integer`     | Indexed                                      |
| `summary`        | `String`      | None                                         |

**Notes:**  
- **Primary Key**: Composite (`product_id`, `scan_id`)  
- **Foreign Key**: `scan_id` references `scan_db(scan_id)` with `ON DELETE CASCADE`

---

### **fres_db**
| Column Name      | Data Type     | Constraints                                   |
|------------------|---------------|-----------------------------------------------|
| `product_id`     | `Integer`     | Primary Key (composite)                      |
| `scan_id`        | `String`      | Foreign Key (references `scan_db.scan_id`), Primary Key (composite) |
| `produce`        | `String`      | None                                         |
| `freshness`      | `Float`       | None                                         |
| `shelf_life`     | `Integer`     | Indexed                                      |

**Table Constraints:**  
- **Primary Key**: Composite (`product_id`, `scan_id`)  
- **Foreign Key**: `scan_id` references `scan_db(scan_id)` with `ON DELETE CASCADE`
