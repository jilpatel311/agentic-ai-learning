import os
import json
import math
from collections import Counter
from flask import Flask, request, jsonify, render_template_string
from flasgger import Swagger
from dotenv import load_dotenv
from groq import Groq
from PyPDF2 import PdfReader
import io

load_dotenv()
app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "RAG Ingestion API",
        "description": "A simple Flask API for ingesting documents, indexing text chunks, and querying with a RAG chatbot.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"]
}

Swagger(app, template=swagger_template)

DOCS_FOLDER = "docs"
INDEX_FILE = "index.json"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# In-memory store
chunks_store = []
tfidf_store = []


# --- RAG Utilities ---

def tokenize(text):
    return [w.lower().strip(".,!?;:\"'()[]{}") for w in text.split() if len(w) > 1]


def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def compute_tfidf(chunks):
    doc_freq = Counter()
    chunk_tokens = []
    for chunk in chunks:
        tokens = tokenize(chunk)
        chunk_tokens.append(tokens)
        for token in set(tokens):
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
    common = set(vec1.keys()) & set(vec2.keys())
    dot = sum(vec1[w] * vec2[w] for w in common)
    mag1 = math.sqrt(sum(v * v for v in vec1.values()))
    mag2 = math.sqrt(sum(v * v for v in vec2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def search_chunks(query, top_k=3):
    if not chunks_store:
        return []
    query_tokens = tokenize(query)
    query_tf = Counter(query_tokens)
    total = len(query_tokens) if query_tokens else 1
    query_vec = {w: count / total for w, count in query_tf.items()}

    scores = []
    for i, vec in enumerate(tfidf_store):
        score = cosine_similarity(query_vec, vec)
        scores.append((score, i))

    scores.sort(reverse=True)
    return [chunks_store[i] for s, i in scores[:top_k] if s > 0]


def rebuild_index():
    global tfidf_store
    tfidf_store = compute_tfidf(chunks_store) if chunks_store else []


def save_index():
    with open(INDEX_FILE, "w") as f:
        json.dump(chunks_store, f)


def load_index():
    global chunks_store
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            chunks_store = json.load(f)
        rebuild_index()


# --- HTML Upload Page ---

UPLOAD_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>RAG Document Upload</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .upload-box { border: 2px dashed #ccc; padding: 40px; text-align: center; border-radius: 10px; margin: 20px 0; }
        .upload-box:hover { border-color: #666; background: #f9f9f9; }
        input[type="file"] { margin: 10px 0; }
        button { background: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #45a049; }
        .result { margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px; display: none; }
        .info { color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <h1>RAG Document Upload</h1>
    <p class="info">Upload PDF or TXT files to ingest into the RAG system.</p>
    
    <div class="upload-box">
        <form id="uploadForm" enctype="multipart/form-data">
            <p>Select a file to upload:</p>
            <input type="file" id="fileInput" name="file" accept=".pdf,.txt">
            <br><br>
            <button type="submit">Upload & Ingest</button>
        </form>
    </div>
    
    <div class="result" id="result"></div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('fileInput');
            if (!fileInput.files.length) { alert('Please select a file'); return; }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = 'Uploading...';
            
            const res = await fetch('/ingest/file', { method: 'POST', body: formData });
            const data = await res.json();
            
            if (res.ok) {
                resultDiv.innerHTML = '<b>Success!</b><br>' + data.message + '<br>Chunks added: ' + data.chunks_added + '<br>Total chunks: ' + data.total_chunks;
            } else {
                resultDiv.innerHTML = '<b>Error:</b> ' + data.error;
            }
        });
    </script>
</body>
</html>
"""


# --- API Endpoints ---

@app.route("/", methods=["GET"])
def upload_page():
    """Serve the upload UI."""
    return render_template_string(UPLOAD_PAGE)


@app.route("/ingest/text", methods=["POST"])
def ingest_text():
    """Ingest raw text directly.
    ---
    tags:
      - ingestion
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
            chunk_size:
              type: integer
            overlap:
              type: integer
    responses:
      200:
        description: Text ingested successfully
        schema:
          type: object
          properties:
            message:
              type: string
            chunks_added:
              type: integer
            total_chunks:
              type: integer
      400:
        description: Missing or invalid request data
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field in request body"}), 400

    text = data["text"]
    chunk_size = data.get("chunk_size", 200)
    overlap = data.get("overlap", 50)

    new_chunks = chunk_text(text, chunk_size, overlap)
    chunks_store.extend(new_chunks)
    rebuild_index()
    save_index()

    return jsonify({
        "message": "Text ingested successfully",
        "chunks_added": len(new_chunks),
        "total_chunks": len(chunks_store)
    })


@app.route("/ingest/file", methods=["POST"])
def ingest_file():
    """Ingest a PDF or TXT file upload.
    ---
    tags:
      - ingestion
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      - name: chunk_size
        in: formData
        type: integer
        required: false
      - name: overlap
        in: formData
        type: integer
        required: false
    responses:
      200:
        description: File ingested successfully
        schema:
          type: object
          properties:
            message:
              type: string
            chunks_added:
              type: integer
            total_chunks:
              type: integer
      400:
        description: Invalid file upload or unsupported file type
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Use 'file' field."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = file.filename.lower()

    # Extract text based on file type
    if filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif filename.endswith(".txt"):
        text = file.read().decode("utf-8")
    else:
        return jsonify({"error": "Unsupported file type. Upload .pdf or .txt files."}), 400

    if not text.strip():
        return jsonify({"error": "No text could be extracted from the file."}), 400

    chunk_size = int(request.form.get("chunk_size", 200))
    overlap = int(request.form.get("overlap", 50))

    new_chunks = chunk_text(text, chunk_size, overlap)
    chunks_store.extend(new_chunks)
    rebuild_index()
    save_index()

    return jsonify({
        "message": f"File '{file.filename}' ingested successfully",
        "chunks_added": len(new_chunks),
        "total_chunks": len(chunks_store)
    })


@app.route("/ingest/folder", methods=["POST"])
def ingest_folder():
    """Ingest all .txt files from the docs/ folder.
    ---
    tags:
      - ingestion
    responses:
      200:
        description: Folder ingested successfully
        schema:
          type: object
          properties:
            message:
              type: string
            total_chunks:
              type: integer
      404:
        description: docs folder not found
    """
    global chunks_store
    chunks_store = []

    if not os.path.exists(DOCS_FOLDER):
        return jsonify({"error": f"Folder '{DOCS_FOLDER}' not found"}), 404

    files_ingested = 0
    for filename in os.listdir(DOCS_FOLDER):
        if filename.endswith(".txt"):
            with open(os.path.join(DOCS_FOLDER, filename), "r") as f:
                text = f.read()
            new_chunks = chunk_text(text)
            chunks_store.extend(new_chunks)
            files_ingested += 1

    rebuild_index()
    save_index()

    return jsonify({
        "message": f"Ingested {files_ingested} file(s) from '{DOCS_FOLDER}/'",
        "total_chunks": len(chunks_store)
    })


@app.route("/query", methods=["POST"])
def query():
    """Query the RAG system — retrieves context and generates an answer.
    ---
    tags:
      - query
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            question:
              type: string
            top_k:
              type: integer
    responses:
      200:
        description: Query answered successfully
        schema:
          type: object
          properties:
            answer:
              type: string
      400:
        description: Missing question field
    """
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400

    question = data["question"]
    top_k = data.get("top_k", 3)

    relevant = search_chunks(question, top_k)
    context = "\n\n".join(relevant) if relevant else "No relevant documents found."

    system_msg = (
        "You are a helpful assistant. Answer the user's question based on the provided context. "
        "If the context doesn't contain the answer, say so and answer from your general knowledge.\n\n"
        f"Context:\n{context}"
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
    )
    answer = response.choices[0].message.content

    return jsonify({
        "answer": answer
    })


@app.route("/chunks", methods=["GET"])
def list_chunks():
    """List all stored chunks.
    ---
    tags:
      - status
    responses:
      200:
        description: List of stored chunks
        schema:
          type: object
          properties:
            total_chunks:
              type: integer
            chunks:
              type: array
              items:
                type: string
    """
    return jsonify({
        "total_chunks": len(chunks_store),
        "chunks": chunks_store
    })


@app.route("/clear", methods=["DELETE"])
def clear_index():
    """Clear all ingested data.
    ---
    tags:
      - status
    responses:
      200:
        description: Index cleared successfully
        schema:
          type: object
          properties:
            message:
              type: string
    """
    global chunks_store, tfidf_store
    chunks_store = []
    tfidf_store = []
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
    return jsonify({"message": "Index cleared"})


if __name__ == "__main__":
    load_index()
    print("RAG Ingestion API running on http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /ingest/text   - Ingest raw text (JSON: {\"text\": \"...\"})")
    print("  POST /ingest/file   - Upload a .txt file")
    print("  POST /ingest/folder - Ingest all files from docs/ folder")
    print("  POST /query         - Ask a question (JSON: {\"question\": \"...\"})")
    print("  GET  /chunks        - List all chunks")
    print("  DELETE /clear       - Clear the index")
    app.run(debug=True, port=5001)
