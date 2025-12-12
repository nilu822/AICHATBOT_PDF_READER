from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

client = QdrantClient(":memory:")

collection_name = "documents"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
)

def store_embeddings(chunks, vectors):
    points = []
    for chunk, vector in zip(chunks, vectors):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": chunk}
        ))
    client.upsert(collection_name=collection_name, points=points)

def search(query_vector):
    response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=3
    )
    return [p.payload["text"] for p in response.points]
