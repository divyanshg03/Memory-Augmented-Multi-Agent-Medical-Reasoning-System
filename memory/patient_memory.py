import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    VectorParams,
    Distance,
    PayloadSchemaType,
    Filter,
    FieldCondition,
)

from memory.embeder import Embedder
from memory.patient_schema import PatientProfile

load_dotenv()


class PatientMemory:
    def __init__(self, collection_name="patient_profiles"):
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

        # ---- REQUIRED INDEXES FOR IDENTITY MATCHING ----
        client.create_payload_index(
            collection_name=self.collection,
            field_name="patient_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        client.create_payload_index(
            collection_name=self.collection,
            field_name="name",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        client.create_payload_index(
            collection_name=self.collection,
            field_name="age",
            field_schema=PayloadSchemaType.INTEGER,
        )

        client.create_payload_index(
            collection_name=self.collection,
            field_name="gender",
            field_schema=PayloadSchemaType.KEYWORD,
        )

    # ---------- Core logic ----------

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

    def get_patient(self, patient_id: str) -> PatientProfile | None:
        results = self.client().retrieve(
            collection_name=self.collection,
            ids=[patient_id],
        )

        if not results:
            return None

        return PatientProfile(**results[0].payload)

    # ---------- NEW: Identity resolution ----------

    def find_patient(self, name: str, age: int, gender: str) -> PatientProfile | None:
        """
        Find an existing patient using stable identity attributes.
        """

        query_filter = Filter(
            must=[
                FieldCondition(key="name", match={"value": name}),
                FieldCondition(key="age", match={"value": age}),
                FieldCondition(key="gender", match={"value": gender}),
            ]
        )

        results, _ = self.client().scroll(
            collection_name=self.collection,
            scroll_filter=query_filter,
            limit=1,
        )

        if not results:
            return None

        return PatientProfile(**results[0].payload)

    def get_or_create_patient(self, patient_data: dict) -> PatientProfile:
        """
        Reuse existing patient if found, else create a new one.
        """

        existing = self.find_patient(
            name=patient_data["name"],
            age=patient_data["age"],
            gender=patient_data["gender"],
        )

        if existing:
            return existing

        patient = PatientProfile(**patient_data)
        self.store_patient(patient)
        return patient
