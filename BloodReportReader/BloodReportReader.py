import pytesseract
import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from PIL import Image

# ------------------ SETUP ------------------

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ------------------ PROMPTS ------------------

NORMALIZATION_PROMPT = """You are a medical document text normalizer.
[TRUNCATED FOR BREVITY — KEEP YOUR FULL PROMPT HERE]
"""

JSON_EXTRACTION_PROMPT = """You are a medical lab report data extraction system.
[KEEP YOUR FULL PROMPT HERE]
"""

# ------------------ FUNCTIONS ------------------

def extract_text_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)


def normalize_ocr_with_langchain(ocr_text: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", NORMALIZATION_PROMPT),
        ("human", "{ocr_text}")
    ])

    chain = prompt | llm
    response = chain.invoke({"ocr_text": ocr_text})

    return response.content.strip()


def extract_json(normalized_text: str) -> dict:
    with open("schema.json", "r") as f:
        schema = json.load(f)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", JSON_EXTRACTION_PROMPT),
        ("human", "Schema:\n{schema}\n\nText:\n{normalized_text}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "schema": json.dumps(schema, indent=2),
        "normalized_text": normalized_text
    })

    return json.loads(response.content)


def save_json(data: dict, directory="data/blood_reports", filename="blood_report.json"):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path


def run_blood_report_pipeline(image_path: str):
    print("🔍 OCR...")
    raw_text = extract_text_from_image(image_path)

    print("🧹 Normalizing...")
    normalized = normalize_ocr_with_langchain(raw_text)

    print("🧠 Structuring JSON...")
    structured = extract_json(normalized)

    print("💾 Saving JSON...")
    path = save_json(structured)

    return path, structured


# ------------------ ENTRY POINT ------------------

if __name__ == "__main__":
    image_path = "bloodReport.png"  # CHANGE IF NEEDED

    print("🚀 Running Blood Report Pipeline")
    saved_path, result = run_blood_report_pipeline(image_path)

    print("✅ Done")
    print("📁 Saved at:", saved_path)
    print(json.dumps(result, indent=2))
