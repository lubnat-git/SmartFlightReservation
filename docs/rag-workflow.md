\# Retrieval-Augmented Generation (RAG) Workflow



```mermaid

flowchart TD

&#x20;   A\[User Question] --> B\[FastAPI Assistant Endpoint]

&#x20;   B --> C\[RAG Pipeline]

&#x20;   C --> D\[Sentence Transformer Embeddings]

&#x20;   D --> E\[FAISS Similarity Search]

&#x20;   E --> F\[Retrieve Relevant Knowledge Chunks]

&#x20;   F --> G{Relevant Context Found?}

&#x20;   G -->|No| H\[Return Fallback Response]

&#x20;   G -->|Yes| I\[Build Grounded Prompt]

&#x20;   I --> J\[Qwen3 LLM via Ollama]

&#x20;   J --> K\[Generate Answer]

&#x20;   K --> L\[Return Answer and Source References]

