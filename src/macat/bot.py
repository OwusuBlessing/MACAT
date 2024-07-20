
from openai import OpenAI
from src.macat.prompts import get_topic_model_prompt,get_summarization_prompt,get_formatting_prompt
from dotenv import load_dotenv
import os
load_dotenv()

key = os.getenv("OPENAI_API_KEY2")
client = OpenAI(api_key=key)


def refine_transcription(transcription: str,role:str):
    roles = ["refine","summarize","format"]

    if role == "refine":
      prompt = get_topic_model_prompt()
    elif role == "summarize":
       prompt = get_summarization_prompt()
    
    elif role == "format":
       prompt = get_formatting_prompt()

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages= [
        {"role": "system", "content": f"{prompt}"},
        {"role": "user", "content": f"Transcription is :{transcription}"}])
    
    return completion.choices[0].message.content



