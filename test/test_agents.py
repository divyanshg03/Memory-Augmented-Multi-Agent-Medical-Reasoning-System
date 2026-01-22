from agents.agent_loop import AgentLoop
from agents.consensus import synthesize_decision
from memory.case_context import build_case_context

# Example case context from Step 3
episode_summary = (
    "Symptoms: sudden fear, heart racing, shortness of breath, dizziness. "
    "Duration: 10 minutes. Severity: 7/10."
)

patient_history = []
population_cases = []

case_context = build_case_context(
    episode_summary,
    patient_history,
    population_cases,
)

loop = AgentLoop()
agent_summary = loop.run(case_context)

final_decision = synthesize_decision(case_context, agent_summary)

print("\nFINAL OUTPUT:\n")
print(final_decision)
