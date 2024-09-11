from langchain.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain.chains import LLMChain

def get_gpt_formatted_text(text):
    template = """
    Given the following text:
    {text}
    
    Extract key product metadata such as name, price, net weight, brand, and quantity.
    Format it as JSON.
    """
    prompt = PromptTemplate(template=template, input_variables=["text"])
    llm = OpenAI()
    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run({"text": text})
