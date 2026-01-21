import json
from agents.specialists import (
    PsychiatryAgent,
    CardiologyAgent,
    NeurologyAgent,
    SafetyAgent,
)


class AgentLoop:
    def __init__(self):
        self.agents = [
            PsychiatryAgent(),
            CardiologyAgent(),
            NeurologyAgent(),
            SafetyAgent(),
        ]

    def run(self, case_context: str, rounds: int = 2) -> dict:
        """
        Run agents in iterative rounds and synthesize consensus.
        """

        agent_outputs = []

        for round_idx in range(rounds):
            round_results = []

            for agent in self.agents:
                result = agent.reason(case_context)
                round_results.append({
                    "agent": agent.role,
                    "output": result,
                })

            agent_outputs.append(round_results)

            # Inject peer opinions into context (lightweight)
            case_context += "\n\nPEER OPINIONS:\n"
            for r in round_results:
                case_context += f"- {r['agent']}: {r['output']}\n"

        return self.summarize(agent_outputs)

    def summarize(self, agent_outputs: list) -> dict:
        """
        Final synthesis across agents.
        """
        flat = [r for round in agent_outputs for r in round]

        disagreements = [
            r for r in flat if "true" in r["output"].lower()
        ]

        consensus = {
            "agent_count": len(flat),
            "disagreements": len(disagreements),
            "raw_opinions": flat,
        }

        return consensus
