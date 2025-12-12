from .loader import extract_text_from_pdf
from .vector_db import store_embeddings, search
from .embedder import embed_text
from ollama import Client

client = Client()   # local Ollama client


def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def load_pdf_and_store(pdf_bytes):
    text = extract_text_from_pdf(pdf_bytes)
    chunks = chunk_text(text)
    vectors = embed_text(chunks)
    store_embeddings(chunks, vectors)


#def answer_query(query):
#    query_vector = embed_text([query])[0]
#   context_chunks = search(query_vector)
#   context = "\n\n".join(context_chunks)

#   prompt = f"""
#You are an AI assistant. Use the below context to answer the question accurately.

#Context:
#{context}

#Question: {query}

#Answer:
#"""

#    response = client.chat(
#        model="llama3.2",         # You can change this
#        messages=[{"role": "user", "content": prompt}]
#    )

#    return response['message']['content']
def answer_query(query):
    # Embed user query
    query_vector = embed_text([query])[0]

    # Search in vector database
    context_chunks = search(query_vector)

    # If context is empty → no matching PDF content
    if not context_chunks:
        print("No PDF context found! Switching to normal chat mode...")

        response = client.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": query}]
        )
        return response['message']['content']

    # Else → RAG answer using PDF
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant. Use the context below *only if it is relevant*.
If not relevant, answer normally.

Context:
{context}

Question: {query}

Answer:
"""

    response = client.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']

