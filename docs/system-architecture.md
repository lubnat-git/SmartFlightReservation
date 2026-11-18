

\# System Architecture



```mermaid

flowchart TD

&#x20;   U\[User] --> F\[Frontend - HTML, CSS, JavaScript]

&#x20;   F --> API\[FastAPI Backend]



&#x20;   API --> AUTH\[Authentication Routes]

&#x20;   API --> FL\[Flight Routes]

&#x20;   API --> BK\[Booking Routes]

&#x20;   API --> PAY\[Payment Routes]

&#x20;   API --> RAG\[AI Assistant Route]

&#x20;   API --> AG\[AI Agent Route]



&#x20;   AUTH --> DB\[(MySQL Database)]

&#x20;   FL --> DB

&#x20;   BK --> DB

&#x20;   PAY --> DB



&#x20;   RAG --> RP\[RAG Pipeline]

&#x20;   RP --> FAISS\[FAISS Vector Search]

&#x20;   FAISS --> KB\[Travel Knowledge Base]

&#x20;   RP --> LLM\[Qwen3 via Ollama]



&#x20;   AG --> AC\[AI Agent Controller]

&#x20;   AC --> LLM

&#x20;   AC --> TOOLS\[Controlled Python Flight Tools]

&#x20;   TOOLS --> FL

&#x20;   TOOLS --> DB

```



\## Architecture Description



The frontend communicates with the FastAPI backend through HTTP APIs.



The backend manages authentication, flight search, bookings, and simulated payments using MySQL.



The AI Travel Assistant retrieves relevant travel information through FAISS and uses the local Qwen3 language model to generate grounded responses.



The AI Flight Agent uses Qwen3 to select from controlled Python tools that reuse the existing flight-search and database functionality.



Booking and payment operations remain under the application's existing user-controlled workflows.



