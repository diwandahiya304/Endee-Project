import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

def embed_texts(texts):
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()

def embed_single(text):
    embedding = model.encode([text])
    return embedding[0].tolist()