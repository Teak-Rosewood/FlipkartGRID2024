from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate

import os
import json

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



