# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Pre-download models
RUN python -c "import torch; \
                from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection; \
                model_id = 'IDEA-Research/grounding-dino-tiny'; \
                device = 'cuda' if torch.cuda.is_available() else 'cpu'; \
                AutoProcessor.from_pretrained(model_id); \
                AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device)"

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy the rest of the application code into the container
COPY count_dino.py .

# Expose any ports the app is expected to run on
EXPOSE 7860

# Run supervisord
CMD ["python", "count_dino.py"]
# CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]