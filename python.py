import os
import math
from collections import Counter
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
DOCS_FOLDER = "docs"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# --- Simple RAG: load, chunk, search ---

def load_documents(folder):
    """Read all .txt files from the docs folder."""
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r") as f:
                docs.append({"name": filename, "content": f.read()})
    return docs


def chunk_text(text, chunk_size=200, overlap=50):
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def tokenize(text):
    """Simple word tokenization."""
    return [w.lower().strip(".,!?;:\"'()[]{}") for w in text.split() if len(w) > 1]


def compute_tfidf(chunks):
    """Compute TF-IDF vectors for all chunks."""
    doc_freq = Counter()
    chunk_tokens = []
    for chunk in chunks:
        tokens = tokenize(chunk)
        chunk_tokens.append(tokens)
        unique_tokens = set(tokens)
        for token in unique_tokens:
            doc_freq[token] += 1

    n_docs = len(chunks)
    tfidf_vectors = []
    for tokens in chunk_tokens:
        tf = Counter(tokens)
        total = len(tokens) if tokens else 1
        tfidf = {}
        for word, count in tf.items():
            idf = math.log((n_docs + 1) / (doc_freq[word] + 1)) + 1
            tfidf[word] = (count / total) * idf
        tfidf_vectors.append(tfidf)
    return tfidf_vectors


def cosine_similarity(vec1, vec2):
    """Cosine similarity between two sparse vectors (dicts)."""
    common = set(vec1.keys()) & set(vec2.keys())
    dot = sum(vec1[w] * vec2[w] for w in common)
    mag1 = math.sqrt(sum(v * v for v in vec1.values()))
    mag2 = math.sqrt(sum(v * v for v in vec2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def search(query, chunks, tfidf_vectors, top_k=3):
    """Find the most relevant chunks for a query."""
    query_tokens = tokenize(query)
    query_tf = Counter(query_tokens)
    total = len(query_tokens) if query_tokens else 1
    query_vec = {w: count / total for w, count in query_tf.items()}

    scores = []
    for i, vec in enumerate(tfidf_vectors):
        score = cosine_similarity(query_vec, vec)
        scores.append((score, i))

    scores.sort(reverse=True)
    return [chunks[i] for _, i in scores[:top_k] if _ > 0]


# --- Chat with RAG context ---

def chat(user_message, history, chunks, tfidf_vectors):
    relevant = search(user_message, chunks, tfidf_vectors)
    context = "\n\n".join(relevant) if relevant else "No relevant documents found."

    system_msg = (
        "You are a helpful assistant. Answer the user's question based on the provided context. "
        "If the context doesn't contain the answer, say so and answer from your general knowledge.\n\n"
        f"Context:\n{context}"
    )

    messages = [{"role": "system", "content": system_msg}] + history + [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
    )
    assistant_message = response.choices[0].message.content
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": assistant_message})
    return assistant_message


def main():
    # Load and index documents
    print("Loading documents from 'docs/' folder...")
    docs = load_documents(DOCS_FOLDER)
    if not docs:
        print("No .txt files found in 'docs/' folder. Add some text files and try again.")
        return

    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc["content"]))

    print(f"Indexed {len(all_chunks)} chunks from {len(docs)} document(s).")
    tfidf_vectors = compute_tfidf(all_chunks)

    print("RAG Chatbot ready! Type 'quit' to exit.\n")
    history = []

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        reply = chat(user_input, history, all_chunks, tfidf_vectors)
        print(f"Bot: {reply}\n")


if __name__ == "__main__":
    main()
