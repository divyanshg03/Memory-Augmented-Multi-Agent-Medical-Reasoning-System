from memory.qdrant_memory import LongTermMemory
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
memory = LongTermMemory()
memory.initialize()
query = "Patient with chest tightness and anxiety symptoms"

results = memory.retrieve_relevant_episodes(
    query_text="Chest tightness anxiety",
    limit=5,
    min_confidence=0.0,
    domain=None,
    days_back=None,
    allow_disagreement=True,
)

print(results)
print(memory.explain_retrieval(results))


print("Retrieved episodes:")
for r in results:
    print(r)

print("\nExplanation:")
print(memory.explain_retrieval(results))
print(memory.client().count(memory.collection))
