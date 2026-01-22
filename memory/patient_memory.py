import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    VectorParams,
    Distance,
    PayloadSchemaType,
)

from memory.embeder import Embedder
from memory.patient_schema import PatientProfile

load_dotenv()


class PatientMemory:
    def __init__(self, collection_name="patient_profiles"):
        self.collection = collection_name
        self._client = None
        self._embedder = None

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

        # Index for patient lookup
        client.create_payload_index(
            collection_name=self.collection,
            field_name="patient_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )

    def store_patient(self, patient: PatientProfile):
        vector = self.embedder().embed(patient.embedding_text())

        self.client().upsert(
            collection_name=self.collection,
            points=[
                {
                    "id": patient.patient_id,
                    "vector": vector,
                    "payload": patient.payload(),
                }
            ],
        )

    def get_patient(self, patient_id: str) -> dict | None:
        results = self.client().retrieve(
            collection_name=self.collection,
            ids=[patient_id],
        )
        if not results:
            return None
        return results[0].payload
