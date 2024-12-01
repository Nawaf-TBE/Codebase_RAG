from flask import Flask, request, jsonify
from git import Repo
from sentence_transformers import SentenceTransformer
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from pinecone import Pinecone
import os
import hmac
import hashlib

app = Flask(__name__)

# Pinecone and model setup
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "codebase-rag"
GITHUB_WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")  # Set this in your Replit secrets
pinecone = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pinecone.Index(PINECONE_INDEX_NAME)
embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

SUPPORTED_EXTENSIONS = {'.py', '.js', '.tsx', '.jsx', '.ipynb', '.java', '.cpp', '.ts', '.go', '.rs', '.vue', '.swift', '.c', '.h'}

# Clone or pull the repository
def clone_or_pull_repo(repo_url, local_path="/tmp/repo"):
    if os.path.exists(local_path):
        repo = Repo(local_path)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(repo_url, local_path)
    return local_path

# Get file content
def get_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Re-index updated files in Pinecone
def reindex_files(repo_path, namespace):
    # Get list of files
    documents = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if os.path.splitext(file)[1] in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    content = get_file_content(file_path)
                    relative_path = os.path.relpath(file_path, repo_path)
                    documents.append(Document(page_content=content, metadata={"source": relative_path}))
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    # Embed and upsert to Pinecone
    for doc in documents:
        embedding = embedding_model.encode(doc.page_content)
        pinecone_index.upsert(vectors=[{"id": doc.metadata["source"], "values": embedding, "metadata": doc.metadata}], namespace=namespace)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verify webhook signature
    payload = request.data
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 403

    data = request.json
    repo_url = data['repository']['clone_url']
    namespace = data['repository']['full_name']  # Use repo name as namespace

    # Re-index the repository
    repo_path = clone_or_pull_repo(repo_url)
    reindex_files(repo_path, namespace)

    return jsonify({"status": "success"}), 200

# Verify the webhook signature
def verify_signature(payload, signature):
    secret = GITHUB_WEBHOOK_SECRET.encode()
    computed_signature = 'sha256=' + hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_signature, signature)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

