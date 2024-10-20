import cv2
import numpy as np

back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=60, detectShadows=True)

# Function to detect objects and return image with bounding boxes
def detect_objects(image, threshold_distance=100):

    def merge_boxes(boxes, threshold_distance=100):
        if len(boxes) == 0:
            return []
        
        merged_boxes = []
        used_boxes = set()

        for i in range(len(boxes)):
            if i in used_boxes:
                continue
            
            # Initialize the first bounding box
            x_min, y_min, w, h = boxes[i]
            x_max, y_max = x_min + w, y_min + h
            
            for j in range(i + 1, len(boxes)):
                if j in used_boxes:
                    continue

                x2_min, y2_min, w2, h2 = boxes[j]
                x2_max, y2_max = x2_min + w2, y2_min + h2

                # Check if boxes are close to each other or overlapping
                if (x_min - threshold_distance <= x2_max and x_max + threshold_distance >= x2_min) and \
                (y_min - threshold_distance <= y2_max and y_max + threshold_distance >= y2_min):
                    
                    # Update the bounding box to include both
                    x_min = min(x_min, x2_min)
                    y_min = min(y_min, y2_min)
                    x_max = max(x_max, x2_max)
                    y_max = max(y_max, y2_max)

                    used_boxes.add(j)  # Mark the second box as used
            
            # Add the merged bounding box
            merged_boxes.append([x_min, y_min, x_max - x_min, y_max - y_min])
        
        return merged_boxes
    
    global back_sub
    # Apply background subtraction
    fg_mask = back_sub.apply(image)

    # Remove shadows by thresholding the mask
    _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    # Apply morphological operations to reduce noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)  # Remove small noise
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # Fill small holes

    # Find contours (i.e., objects)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []

    # Iterate through contours and collect bounding boxes
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter out small contours
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append([x, y, w, h])

    # Merge close or overlapping bounding boxes
    merged_boxes = merge_boxes(boxes, threshold_distance=threshold_distance)

    # Draw the merged boxes on the image
    for x, y, w, h in merged_boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Return the number of merged boxes and the modified image
    return len(merged_boxes), image
