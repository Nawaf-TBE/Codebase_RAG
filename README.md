# Codebase_RAG

# Codebase RAG Chatbot 🚀

An AI-powered chatbot that enables users to interact with codebases using **Retrieval-Augmented Generation (RAG)**. This project combines the power of **Pinecone**, **OpenAI**, and **Streamlit** to simplify navigating and understanding complex codebases.

---

## 🌟 Features
- **Chat with a Codebase**: Ask questions and get detailed, contextual responses about the codebase.
- **Multiple Codebases**: Easily switch between different projects to query specific repositories.
- **Dynamic Retrieval**: Uses Pinecone to fetch the most relevant parts of the codebase for accurate responses.
- **Simple Interface**: A user-friendly Streamlit web app for seamless interactions.
- **Future-Proof**: Attempts to implement GitHub webhooks for automatic updates to the Pinecone index.

---

## 🛠️ Technologies Used
- **Streamlit**: For the web-based chatbot interface.
- **OpenAI**: For generating AI-powered responses.
- **Pinecone**: For storing and querying code embeddings.
- **SentenceTransformers**: For embedding code files using `all-mpnet-base-v2`.
- **Flask**: To handle GitHub webhook events.

---

## 🚀 How It Works
1. **Codebase Embedding**:
   - Supported file types (e.g., `.py`, `.js`, `.java`) are extracted and embedded using SentenceTransformers.
   - These embeddings are stored in Pinecone for fast retrieval.

2. **Chatbot Interaction**:
   - Users input questions in the web app.
   - The app retrieves relevant code snippets from Pinecone and uses OpenAI to generate responses.

3. **Dynamic Codebase Switching**:
   - A dropdown menu allows users to query different repositories seamlessly.

---

#Challenges and Learnings

Webhook Integration:
Set up a GitHub webhook to automate the re-indexing process.
Encountered challenges in handling partial updates to Pinecone.
Context Limitations:
Managing the amount of data retrieved from Pinecone to ensure efficient processing by the language model.
Error Handling:
Improved debugging skills while dealing with webhook errors and API responses.
Future Improvements

Webhook Completion:
Automate the re-indexing process fully to handle new commits dynamically.
Multimodal RAG:
Add support for image uploads to query image-related data in the codebase.
Enhanced Multi-Codebase Queries:
Allow querying across multiple codebases simultaneously.

 Challenges Faced

Webhook Implementation:
Cloning and embedding new code updates worked, but re-indexing Pinecone for partial updates remains a challenge.
Embedding Large Codebases:
Optimizing performance for large repositories is an ongoing task.

