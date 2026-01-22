import os
from groq import Groq
from dotenv import load_dotenv
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(prompt: str, model="openai/gpt-oss-120b"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_completion_tokens=7000,
        top_p=1,
        reasoning_effort="high",
        stream=False,
        stop=None

    )
    return completion.choices[0].message.content
