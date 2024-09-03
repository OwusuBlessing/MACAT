
from openai import OpenAI
from src.macat.prompts import get_translation_prompt
from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv("OPENAI_API_KEY2")
client = OpenAI(api_key=key)


def get_translation(text: str,language:str):

    prompt = get_translation_prompt()
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages= [
        {"role": "system", "content": f"{prompt}"},
        {"role": "user", "content": f"Text is :{text}, language:{language}"}])
    
    return completion.choices[0].message.content



