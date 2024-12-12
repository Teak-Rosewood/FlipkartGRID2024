from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate
import base64
import requests
import os
import json
from mistralai import Mistral

api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    print("API key not found in environment variables")

# Specify model
model = "pixtral-12b-2409"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

def load_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def get_estimated_shelf_life(fruit, freshness):
    template_path = os.path.join('utils/templates', 'shelf_life.txt')
    template = load_template(template_path)
    model = ChatMistralAI(model="open-mistral-nemo")
    prompt = PromptTemplate(template=template, input_variables=['fruit', 'freshness'])
    chain = prompt | model
    content = chain.invoke({"fruit": fruit, "freshness": freshness}).content.strip()
    print(content)
    try: 
        return json.loads(content)
    except json.JSONDecodeError as e: 
        return "Error in JSON Format"

def get_gpt_formatted_text(text):
    template_path = os.path.join('utils/templates', 'ocr_to_json.txt')
    template = load_template(template_path)
    model = ChatMistralAI(model="open-mistral-nemo")
    prompt = PromptTemplate(template=template, input_variables=['text'])
    chain = prompt | model
    content = chain.invoke({"text": text}).content.strip()
    try: 
        return json.loads(content)
    except json.JSONDecodeError as e: 
        return "Error in JSON Format"

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

def get_pixtral_response(image_path, text = ""):
    """Get the response from the pixtral-12b-2409 model."""
    base64_image = encode_image(image_path)
    if not base64_image:
        return "Error encoding image"
    # Define the messages for the chat
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text":'''
                    This is the image from a packaged product, estimate the information and return a JSON object where:

                    1. If the `brand_product`, is not present, take an educated guess from a list of products you know.
                    2. if the 'expiry_date', is not present, take an educated guess while considering the today's date as 13/12/2024 
                    2. if the 'expired' term, is not present, take an educated guess based on the expiry data
                    2. If `shelf_life` is not provided, set it to `"NA"`.
                    3. If `expired` or `shelf_life` are `"NA"`, predict them from the text or trustable sources and add them to `estimates`.
                    5. Include all details under the `summary` field.
                    6. Note that all these products are sold in India.
78
                    Expected JSON format:
                    {{
                    "brand_product": "[Extracted or 'NA']",
                    "expiry_date": "[Extracted or 'NA']",
                    "expired": "[Extracted as true or false or 'NA']",
                    "shelf_life": "[Extracted or 'NA']",
                    "estimates" : {{
                        expected_shelf_life: "[if shelf_life is NA provide an estimated price in days]"
                        expected_expired: "[if expired is true]"
                    }}
                    "summary" : "[summary of all the details extracted from the image along with estimated values]"
                    }}

                    Return only the JSON object, all in small letters without any additional text or explanation.
                    '''
                },
                {
                    "type": "text",
                    "text": "JSON DATA provided with the image is" + text
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}" 
                }
            ]
        }
    ]

    # Get the chat response
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )

    # Print the content of the response
    content = chat_response.choices[0].message.content
    try: 
        # Clean up the response content
        content = content.replace("```json", "").replace("```", "").strip()
        print(content)
        return json.loads(content)
    except json.JSONDecodeError as e: 
        return "Error in JSON Format"

def process_image_or_text(text=None, image_path=None):
    if text:
        return get_gpt_formatted_text(text)
    elif image_path:
        return get_pixtral_response(image_path)
    else:
        return "No input provided"



