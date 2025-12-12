from ollama import Client
client = Client()

def embed_text(chunks):
    vectors = []
    for text in chunks:
        emb = client.embeddings(model="llama3.2", prompt=text)
        vectors.append(emb["embedding"])
    return vectors
