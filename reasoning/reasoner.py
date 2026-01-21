from llm.groq_client import call_groq


class MemoryAwareReasoner:
    def __init__(self, memory):
        self.memory = memory

    def reason(self, query: str, domain: str | None = None) -> dict:
        # 1. Retrieve long-term memory
        retrieved = self.memory.retrieve_relevant_episodes(
            query_text=query,
            limit=3,
            min_confidence=0.7,
            domain=domain,
            days_back=365,
            allow_disagreement=True,
        )

        # 2. Build memory context
        if retrieved:
            memory_block = ""
            for i, ep in enumerate(retrieved, 1):
                memory_block += (
                    f"{i}. Past decision: {ep['decision']}\n"
                    f"   Reasoning factors: {', '.join(ep['reasoning_factors'])}\n"
                    f"   Confidence: {ep['confidence']}\n\n"
                )

            memory_instruction = (
                "You have access to relevant long-term memory from past reasoning episodes. "
                "Use it as supporting evidence, not as absolute truth."
            )
        else:
            memory_block = "No relevant long-term memory was found."
            memory_instruction = (
                "There is no relevant long-term memory available. "
                "Proceed cautiously and explicitly acknowledge uncertainty."
            )

        # 3. Groq prompt (THIS IS IMPORTANT)
        prompt = f"""
You are a decision-support reasoning system.

{memory_instruction}

LONG-TERM MEMORY:
{memory_block}

CURRENT QUERY:
{query}

INSTRUCTIONS:
- Reason step-by-step internally.
- Do NOT hallucinate past cases.
- If memory is weak or absent, explicitly say so.
- Produce a concise, structured answer.
"""

        # 4. Call Groq
        response = call_groq(prompt)

        return {
            "query": query,
            "used_memory": bool(retrieved),
            "retrieved_episodes": retrieved,
            "response": response,
        }
