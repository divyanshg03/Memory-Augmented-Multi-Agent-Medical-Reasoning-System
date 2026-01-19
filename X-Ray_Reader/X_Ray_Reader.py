import base64
import json
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

# ------------------ IMAGE UTILS ------------------

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ------------------ XRAY READING ------------------

XRAY_PROMPT = """
You are a radiology report assistant.

Analyze the provided X-ray image and describe visible findings.
Do not diagnose or suggest treatment.
Use observational medical language only.
"""


def read_xray(image_path: str) -> str:
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0
    )

    image_base64 = encode_image(image_path)

    message = HumanMessage(
        content=[
            {"type": "text", "text": XRAY_PROMPT},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_base64}"
                }
            }
        ]
    )

    response = llm.invoke([message])
    return response.content.strip()


# ------------------ XRAY JSON STRUCTURING ------------------

XRAY_JSON_PROMPT = """
You are a radiology findings structuring system.

Your task:
- Convert X-ray findings text into structured JSON
- Use ONLY the provided schema

Rules:
- Do NOT diagnose conditions
- Do NOT add findings not present in the text
- Group findings under lungs, heart, pleura, bones
- Preserve original sentences in "raw_text"
- Summarize each section concisely in "findings"
- If uncertainty is present, add to "uncertain_findings"

Output:
- Return ONLY valid JSON
"""


def xray_findings_to_json(findings_text: str) -> dict:
    with open("xray_schema.json", "r") as f:
        schema = json.load(f)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", XRAY_JSON_PROMPT),
        ("human", "Schema:\n{schema}\n\nFindings:\n{findings_text}")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "schema": json.dumps(schema, indent=2),
        "findings_text": findings_text
    })

    return json.loads(response.content)


# ------------------ PIPELINE ORCHESTRATOR ------------------

def run_xray_pipeline(image_path: str) -> dict:
    print("🩻 Reading X-ray image...")
    findings = read_xray(image_path)

    print("🧠 Structuring findings into JSON...")
    structured = xray_findings_to_json(findings)

    return structured


# ------------------ ENTRY POINT ------------------

if __name__ == "__main__":
    image_path = "fractureBone2.jpg"  # CHANGE IF NEEDED

    print("🚀 Running X-ray Pipeline")
    result = run_xray_pipeline(image_path)

    print("✅ Pipeline finished")
    print(json.dumps(result, indent=2))
