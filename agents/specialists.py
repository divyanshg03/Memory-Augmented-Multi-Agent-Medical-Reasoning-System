from llm.groq_client import call_groq


class BaseAgent:
    role = "general"

    def reason(self, case_context: str) -> dict:
        prompt = f"""
You are a medical specialist acting as a {self.role} expert.

CASE CONTEXT:
{case_context}

INSTRUCTIONS:
- Give your assessment from your specialty perspective.
- Mention key supporting or contradicting evidence.
- State your confidence (0–1).
- Flag if you disagree with other possible interpretations.
- Do NOT make absolute claims.

Respond in JSON with keys:
assessment, reasoning, confidence, disagreement
"""
        response = call_groq(prompt)
        return response


class PsychiatryAgent(BaseAgent):
    role = "psychiatry"


class CardiologyAgent(BaseAgent):
    role = "cardiology"


class NeurologyAgent(BaseAgent):
    role = "neurology"


class SafetyAgent(BaseAgent):
    role = "risk and safety"
