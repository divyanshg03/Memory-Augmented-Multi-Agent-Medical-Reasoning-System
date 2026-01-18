import os
from groq import Groq
from dotenv import load_dotenv
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(prompt: str, model="llama-3.1-70b-versatile"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content
