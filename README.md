# Codebase_RAG

#Overview

This project is an AI-powered chatbot that enables users to interact with codebases using Retrieval-Augmented Generation (RAG). It leverages Pinecone for vector-based search and OpenAI's language models to provide meaningful insights about a codebase, making it easier for developers to navigate and understand complex projects.

#Features

Codebase Querying:
Ask questions about the structure, functionality, or specific files in a codebase.
Retrieve the most relevant code snippets to generate accurate, detailed answers.
Multi-Codebase Support:
Switch between different codebases using a dropdown menu.
Dynamic Search:
Uses Pinecone to store and search embeddings for fast and efficient retrieval.
Streamlit Interface:
A simple and user-friendly web app for querying and interacting with the chatbot.
Webhook Setup Attempt:
Explored automating the re-indexing process using GitHub webhooks to update the Pinecone database on new commits. Although not fully implemented, the foundation for this feature has been established.



#Tech Stack

Python: Core programming language.
Streamlit: Front-end for the chatbot interface.
Pinecone: Vector database for embedding and retrieval.
OpenAI: Large language models for response generation.
Flask: Backend framework for webhook integration (attempted).
How It Works

Embedding the Codebase:
The codebase is cloned locally, and supported files are processed to extract content.
The extracted content is converted into embeddings using the sentence-transformers model and stored in Pinecone.
Query Processing:
A user inputs a question through the Streamlit app.
The chatbot retrieves the most relevant context from Pinecone based on the query embedding.
OpenAI’s language model generates a response based on the retrieved context.
Multi-Codebase Support:
Users can select a specific codebase to query.
The app dynamically adjusts the namespace in Pinecone to fetch relevant data.
Webhook Setup (Attempted):
Explored automating updates to the Pinecone index using GitHub webhooks.
Set up a webhook to listen for push events and trigger re-embedding of updated files.

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
