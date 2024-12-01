import streamlit as st
from sentence_transformers import SentenceTransformer
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import HuggingFaceEmbeddings
from openai import OpenAI
from pinecone import Pinecone
import os

# Initialize Pinecone and OpenAI
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

pinecone = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pinecone.Index("codebase-rag")
vectorstore = PineconeVectorStore(index_name="codebase-rag", embedding=HuggingFaceEmbeddings())

openai_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# Embedding Model
def get_huggingface_embeddings(text, model_name="sentence-transformers/all-mpnet-base-v2"):
    model = SentenceTransformer(model_name)
    return model.encode(text)

# Perform RAG Query
def perform_rag(query, namespace):
    raw_query_embedding = get_huggingface_embeddings(query)

    # Query Pinecone for relevant context
    top_matches = pinecone_index.query(
        vector=raw_query_embedding.tolist(),
        top_k=5,
        include_metadata=True,
        namespace=namespace
    )

    # Extract context from Pinecone results
    contexts = [item['metadata']['text'] for item in top_matches['matches']]
    augmented_query = "<CONTEXT>\n" + "\n\n-------\n\n".join(contexts[:10]) + "\n-------\n</CONTEXT>\n\nMY QUESTION:\n" + query

    # Chat with the codebase
    system_prompt = """You are a Senior Software Engineer, specializing in TypeScript.
    Answer any questions I have about the codebase, based on the code provided. Always consider all of the context provided when forming a response."""

    llm_response = openai_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": augmented_query}
        ]
    )

    return llm_response.choices[0].message.content

# Streamlit UI
st.title("Codebase RAG Chatbot")
st.markdown("Chat with your codebase using Retrieval-Augmented Generation (RAG).")

# Codebase selection
codebases = {
    "SecureAgent": "https://github.com/CoderAgent/SecureAgent",
    "ExampleProject": "example-namespace",
    # Add more codebases here
}
selected_codebase = st.selectbox("Select a codebase:", list(codebases.keys()))

# User input for queries
query = st.text_input("Enter your question:", placeholder="E.g., How are Python files parsed?")
if st.button("Submit"):
    if query:
        with st.spinner("Processing your query..."):
            try:
                namespace = codebases[selected_codebase]
                response = perform_rag(query, namespace)
                st.markdown("### Response:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")

st.markdown("Built with ❤️ using Streamlit, Pinecone, and OpenAI.")
