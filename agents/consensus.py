from llm.groq_client import call_groq


def synthesize_decision(case_context: str, agent_summary: dict) -> str:
    prompt = f"""
You are a senior clinician synthesizing opinions from multiple specialists.

CASE CONTEXT:
{case_context}

AGENT SUMMARY:
{agent_summary}

INSTRUCTIONS:
- Produce a final assessment.
- Mention level of certainty.
- Highlight unresolved disagreements.
- Recommend next steps cautiously.
- DO NOT claim definitive diagnosis.

Return a concise structured answer.
"""
    return call_groq(prompt)
