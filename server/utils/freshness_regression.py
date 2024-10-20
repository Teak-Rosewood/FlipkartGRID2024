import cv2
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input

pretrained_model = ResNet50(
    include_top=False,
    input_shape=(180, 180, 3),
    pooling='avg',
    weights='imagenet'
)

inputs = layers.Input(shape=(180, 180, 3))
x = pretrained_model(inputs)
x = layers.Dense(512, activation='relu')(x)
outputs = layers.Dense(12, activation='softmax')(x)
model = models.Model(inputs, outputs)
model.load_weights("models/resnet_model_weights.weights.h5")

# Preprocess the OpenCV image for the ResNet model
def preprocess_image(image):
    image = cv2.resize(image, (180, 180))
    image = np.array(image, dtype=np.float32)
    image = preprocess_input(image)  # Subtracts mean and scales inputs
    image = np.expand_dims(image, axis=0)
    return image

# Predict the class of an image
def predict_class(image):
    global model
    preprocessed_image = preprocess_image(image)
    predictions = model.predict(preprocessed_image)
    rotten = np.sum((predictions[0])[6:])
    return rotten
