import os
os.environ['no_proxy'] = '127.0.0.1,localhost'
os.environ['NO_PROXY'] = '127.0.0.1,localhost'

from endee import Endee, Precision

INDEX_NAME = "doc_qa_index"
DIMENSION = 384

def get_client():
    return Endee()

def create_index_if_not_exists():
    client = get_client()
    try:
        client.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            space_type="cosine",
            precision=Precision.INT8
        )
        print("Index created.")
    except Exception as e:
        print(f"Index note: {e}")

def store_chunks(chunks, embeddings):
    client = get_client()
    index = client.get_index(name=INDEX_NAME)
    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": f"chunk_{i}",
            "vector": embedding,
            "meta": {"text": chunk}
        })
    print(f"Storing {len(vectors)} vectors...")
    result = index.upsert(vectors)
    print(f"Upsert result: {result}")

def search_similar(query_embedding, top_k=5):
    client = get_client()
    try:
        index = client.get_index(name=INDEX_NAME)
        results = index.query(vector=query_embedding, top_k=top_k)
        print(f"Results found: {len(results)}")
        for r in results:
            print(f"Result: {r}")
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

def delete_index():
    client = get_client()
    try:
        client.delete_index(name=INDEX_NAME)
        print("Index deleted.")
    except:
        pass