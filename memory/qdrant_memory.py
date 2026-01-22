import os
import time
from typing import List, Dict

from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    VectorParams,
    Distance,
    Filter,
    FieldCondition,
    Range,
    PayloadSchemaType,
)

from memory.embeder import Embedder
from memory.schema import ReasoningEpisode

load_dotenv()


class LongTermMemory:
    def __init__(self, collection_name="reasoning_episodes"):
        self.collection = collection_name
        self._client = None
        self._embedder = None

    # ---------- Lazy resources ----------

    def client(self) -> QdrantClient:
        if self._client is None:
            self._client = QdrantClient(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY"),
            )
        return self._client

    def embedder(self) -> Embedder:
        if self._embedder is None:
            self._embedder = Embedder()
        return self._embedder

    # ---------- Initialization ----------

    def initialize(self):
        client = self.client()

        if not client.collection_exists(self.collection):
            client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=self.embedder().dim,
                    distance=Distance.COSINE,
                ),
            )

        # ---- REQUIRED PAYLOAD INDEXES ----
        client.create_payload_index(
            collection_name=self.collection,
            field_name="confidence",
            field_schema=PayloadSchemaType.FLOAT,
        )

        client.create_payload_index(
            collection_name=self.collection,
            field_name="timestamp",
            field_schema=PayloadSchemaType.FLOAT,
        )

        client.create_payload_index(
            collection_name=self.collection,
            field_name="domain",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        client.create_payload_index(
            collection_name=self.collection,
            field_name="disagreement",
            field_schema=PayloadSchemaType.BOOL,
        )

    # ---------- Write / Update ----------

    def write_episode(self, episode: ReasoningEpisode):
        vector = self.embedder().embed(episode.embedding_text())

        self.client().upsert(
            collection_name=self.collection,
            points=[
                {
                    "id": episode.episode_id,
                    "vector": vector,
                    "payload": episode.payload(),
                }
            ],
        )

    def update_episode(self, episode_id: str, validated: bool, confidence: float):
        self.client().set_payload(
            collection_name=self.collection,
            payload={
                "validated": validated,
                "confidence": confidence,
            },
            points=[episode_id],
        )

    # ---------- Retrieval ----------

    def retrieve_relevant_episodes(
        self,
        query_text: str,
        limit: int = 5,
        min_confidence: float = 0.7,
        domain: str | None = None,
        days_back: int | None = None,
        allow_disagreement: bool = True,
    ) -> List[Dict]:

        query_vector = self.embedder().embed(query_text)

        must_conditions = [
            FieldCondition(
                key="confidence",
                range=Range(gte=min_confidence),
            )
        ]

        if domain:
            must_conditions.append(
                FieldCondition(
                    key="domain",
                    match={"value": domain},
                )
            )

        if not allow_disagreement:
            must_conditions.append(
                FieldCondition(
                    key="disagreement",
                    match={"value": False},
                )
            )

        if days_back:
            cutoff = time.time() - (days_back * 24 * 60 * 60)
            must_conditions.append(
                FieldCondition(
                    key="timestamp",
                    range=Range(gte=cutoff),
                )
            )

        query_filter = Filter(must=must_conditions)

        results = self.client().query_points(
                collection_name=self.collection,
                query=query_vector,
                query_filter=query_filter,
                limit=limit,
            ).points
    
        return [
                {
                    "episode_id": r.payload["episode_id"],
                    "state_summary": r.payload["state_summary"],
                    "decision": r.payload["decision"],
                    "reasoning_factors": r.payload["reasoning_factors"],
                    "confidence": r.payload["confidence"],
                    "disagreement": r.payload["disagreement"],
                    "score": r.score,
                }
                for r in results
            ]
    
    def explain_retrieval(self, retrieved_episodes):
            """
            Human-readable explanation of why these memories were retrieved.
            This is used for debugging, logging, and later for LLM grounding.
            """
            if not retrieved_episodes:
                return "No relevant past episodes were retrieved."
    
            explanation = (
                "Retrieved past reasoning episodes based on:\n"
                "- Semantic similarity to the current query\n"
                "- Confidence threshold filtering\n"
                "- Contextual payload filters (domain, time, disagreement)\n\n"
            )
    
            for i, ep in enumerate(retrieved_episodes, 1):
                explanation += (
                    f"{i}. Decision: {ep['decision']}\n"
                    f"   Confidence: {ep['confidence']}\n"
                    f"   Similarity score: {round(ep['score'], 3)}\n\n"
                )
    
            return explanation
