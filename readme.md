# AI-Powered Smart Flight Reservation and Travel Intelligence Platform

A full-stack flight reservation application enhanced with Generative AI, Retrieval-Augmented Generation (RAG), semantic knowledge retrieval, and an AI-powered flight search agent.

Built using Python, FastAPI, MySQL, HTML, CSS, JavaScript, FAISS, Sentence Transformers, and a locally hosted Qwen3 language model.

## 1. Project Overview

The Smart Flight Reservation and Travel Intelligence Platform combines traditional flight reservation functionality with AI-powered travel assistance.

Users can register, authenticate, search for flights, reserve seats, make simulated payments, manage bookings, and cancel reservations.

The platform also provides two AI capabilities:

- **AI Travel Assistant:** Answers travel-related questions using a knowledge base and RAG.
- **AI Flight Search Agent:** Understands natural-language flight requests and uses controlled Python tools to search and compare available flights.

The project demonstrates practical backend development, database management, API security, automated testing, and applied Generative AI.

## 2. Problem Statement

Traditional reservation workflows require users to navigate multiple operations to find flights, manage bookings, and obtain travel information.

This project aims to provide an integrated application that:

- Simplifies flight searching and reservations.
- Provides secure user authentication.
- Manages seat availability during bookings.
- Supports booking history and cancellation.
- Provides simulated payment processing.
- Answers travel-related questions using retrieved knowledge.
- Enables natural-language flight search through an AI agent.

## 3. Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.12 |
| Backend | FastAPI |
| Database | MySQL 8.0 |
| Database Connectivity | SQLAlchemy, PyMySQL |
| Database Queries | Parameterized SQL using SQLAlchemy `text()` |
| Frontend | HTML, CSS, JavaScript |
| Authentication | JWT |
| Password Security | Argon2 |
| API Documentation | Swagger UI |
| API Testing | Postman |
| Automated Testing | Pytest |
| LLM Runtime | Ollama |
| Language Model | Qwen3 1.7B |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Search | FAISS |
| AI Architecture | RAG and controlled agentic tool calling |
| Version Control | Git |
| Code Hosting | GitHub |
| Deployment | Local development; Azure deployment subject to free-resource eligibility |

## 4. Implemented Features

### 4.1 User Authentication

- User registration and login.
- Password hashing using Argon2.
- JWT-based authentication.
- Protected user-specific endpoints.
- Input validation for registration and login.

### 4.2 Flight Management

- Retrieve available flights.
- Search flights using source and destination cities.
- Display airline and flight information.
- Display departure and arrival details.
- Display ticket prices and available seats.

### 4.3 Booking Management

- Reserve available flight seats.
- Automatic seat allocation.
- Database transaction and row-locking safeguards during booking.
- Prevent booking when seats are unavailable.
- View booking history.
- Cancel existing reservations.
- Restore seat availability after cancellation.
- Validate booking ownership for booking-management operations.

### 4.4 Payment Management

- Simulated payment processing.
- Supported payment modes:
  - UPI
  - Card
  - Net Banking
  - Cash
- Booking ownership validation.
- Duplicate successful payment prevention.
- Payment status management.

**Important:** Payments are simulated. No real money is transferred and no external payment gateway is integrated.

### 4.5 Generative AI Travel Assistant

A conversational travel assistant that answers questions using the application's travel knowledge base.

Implemented capabilities:

- Natural-language question handling.
- Retrieval of relevant travel information.
- Context-based LLM answer generation.
- Source references in responses.
- Fallback when relevant information is unavailable.
- Empty-input validation.
- Error handling for LLM service failures.

### 4.6 Retrieval-Augmented Generation (RAG)

The RAG pipeline combines semantic retrieval with a locally hosted language model.

Implemented components:

- Travel FAQ and policy knowledge documents.
- Text chunking and preprocessing.
- Sentence Transformer embeddings.
- FAISS vector indexing.
- Similarity-based retrieval.
- Context filtering using a similarity threshold.
- Context-grounded answer generation using Qwen3.

The embedding model is pretrained; this project uses it to generate embeddings rather than training a new machine-learning model.

### 4.7 Agentic AI Flight Search

The AI flight-search agent interprets natural-language requests and selects from a controlled set of Python tools.

Available tools:

- `search_flights` — searches flights by source and destination.
- `compare_flights` — compares flight prices.
- `find_cheapest_flight` — identifies the lowest-priced option.
- `check_seat_availability` — checks available seats for a flight.

The agent uses Qwen3 through Ollama for tool selection and natural-language responses.

Python validates tool arguments and executes only explicitly permitted tools. The tools reuse the existing application backend and database.

**Booking safety:** The AI agent does not independently create bookings, process payments, or cancel reservations. Users must proceed through the existing application booking workflow, which includes authentication, passenger ID validation, and explicit booking confirmation.

## 5. System Architecture

The application follows a client-server architecture with separate AI assistant and AI agent workflows.

### Application architecture

```text
                  USER
                    |
                    v
             FRONTEND
          HTML / CSS / JS
                    |
                    v
              FASTAPI
                    |
       +------------+------------+
       |            |            |
       v            v            v
 Authentication  Flights     Bookings
       |            |            |
       +------------+------------+
                    |
                    v
               MYSQL 8.0
                    |
                    v
             Simulated Payments
```

### RAG architecture

```text
             USER QUESTION
                   |
                   v
          FASTAPI ASSISTANT API
                   |
                   v
             RAG PIPELINE
                   |
                   v
          SEMANTIC RETRIEVAL
                   |
                   v
             FAISS INDEX
                   |
                   v
          RELEVANT KNOWLEDGE
                   |
                   v
          QWEN3 LANGUAGE MODEL
                   |
                   v
             GROUNDED ANSWER
                   |
                   v
             SOURCE REFERENCES
```

### Agentic AI architecture

```text
          NATURAL-LANGUAGE REQUEST
                    |
                    v
             FASTAPI AGENT API
                    |
                    v
             QWEN3 LLM
                    |
                    v
             TOOL SELECTION
                    |
                    v
          PYTHON TOOL VALIDATION
                    |
                    v
          CONTROLLED TOOL EXECUTION
                    |
                    v
          EXISTING BACKEND / MYSQL
                    |
                    v
              TOOL RESULTS
                    |
                    v
             QWEN3 LLM
                    |
                    v
          NATURAL-LANGUAGE RESPONSE
                    |
                    v
             FRONTEND RESULTS
                    |
                    v
        USER-CONTROLLED BOOKING FLOW
```

## 6. Architecture Diagrams

Detailed diagrams are maintained separately in the `docs/` directory.

- [Overall System Architecture](docs/system-architecture.md)
- [Database Entity Relationship Diagram](docs/database-er-diagram.md)
- [RAG Workflow](docs/rag-workflow.md)
- [Agentic AI Workflow](docs/agent-workflow.md)

These diagrams explain the application's architecture, database relationships, knowledge retrieval process, and controlled AI tool execution.

## 7. Project Structure

```text
Smartflightreservation/
|
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- database.py
|   |-- security.py
|   |-- schemas.py
|   |
|   |-- routes/
|       |-- __init__.py
|       |-- auth.py
|       |-- flights.py
|       |-- bookings.py
|       |-- payments.py
|       |-- assistant.py
|       |-- agent.py
|
|-- ai_agent/
|   |-- agent.py
|   |-- flight_tools.py
|
|-- knowledge_base/
|   |-- travel_faq.txt
|   |-- travel_policies.txt
|   |-- build_embeddings.py
|   |-- search_knowledge.py
|   |
|   |-- vector_store/
|       |-- chunks.json
|       |-- knowledge.index
|
|-- frontend/
|   |-- index.html
|   |-- style.css
|   |-- script.js
|
|-- tests/
|   |-- conftest.py
|   |-- test_app.py
|   |-- test_auth.py
|   |-- test_bookings.py
|   |-- test_flights.py
|   |-- test_payments.py
|   |-- test_assistant.py
|   |-- test_agent.py
|   |-- test_schema.sql
|
|-- docs/
|   |-- system-architecture.md
|   |-- database-er-diagram.md
|   |-- rag-workflow.md
|   |-- agent-workflow.md
|
|-- postman/
|-- .postman/
|-- rag_pipeline.py
|-- readme.md
|-- .gitignore
|-- .env (local only)
```

## 8. Installation and Setup

### Prerequisites

- Python 3.12 or later.
- MySQL 8.0 or later.
- Git.
- Ollama.
- A modern web browser.
- Visual Studio Code with Live Server, or another local frontend server.

### Step 1: Clone the repository

```bash
git clone https://github.com/lubnat-git/SmartFlightReservation.git
```

### Step 2: Navigate to the project

```bash
cd SmartFlightReservation
```

### Step 3: Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\activate
```

### Step 4: Install Python dependencies

```bash
python -m pip install fastapi uvicorn sqlalchemy pymysql python-dotenv "pwdlib[argon2]" PyJWT email-validator requests sentence-transformers faiss-cpu pytest
```

### Step 5: Configure environment variables

Create a `.env` file in the project root.

Configure the following variables with your own local MySQL and JWT settings:

```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=flight_system

JWT_SECRET_KEY=your_secure_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use a strong, randomly generated JWT secret. Never commit `.env` or share its values.

### Step 6: Configure MySQL

Create the application database:

```sql
CREATE DATABASE flight_system;
```

Create the required application tables and populate the database with the flight and reference data expected by the application.

The application uses the following database tables:

- users
- passengers
- airports
- flights
- bookings
- payments

Configure the database credentials in `.env` before starting the backend.

### Step 7: Install and start Ollama

Install Ollama from:

https://ollama.com/

Download the configured language model:

```bash
ollama pull qwen3:1.7b
```

Ensure the Ollama local service is running. The application uses:

```text
http://localhost:11434
```

The RAG pipeline and AI flight agent use the local Qwen3 model.

### Step 8: Build the knowledge-base vector index

From the project root, run:

```bash
python knowledge_base/build_embeddings.py
```

This generates the embedding vectors and FAISS index from the travel knowledge documents.

The Sentence Transformer model is downloaded when first needed.

### Step 9: Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

Backend address:

```text
http://127.0.0.1:8000
```

### Step 10: Open API documentation

Visit:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides interactive API documentation and testing.

### Step 11: Start the frontend

Open the `frontend` folder using Visual Studio Code and launch `index.html` with Live Server.

The configured frontend address is:

```text
http://localhost:5500
```

## 9. API Modules

| Module | Endpoint | Functionality |
|---|---|---|
| Authentication | `/auth/register` | User registration |
| Authentication | `/auth/login` | User login |
| Authentication | `/auth/me` | Current authenticated user |
| Flights | `/flights/` | Retrieve flights |
| Flights | `/flights/search` | Search flights |
| Bookings | `/bookings/` | Create booking |
| Bookings | `/bookings/my` | Booking history |
| Bookings | `/bookings/cancel/{booking_id}` | Cancel booking |
| Payments | `/payments/` | Simulated payment |
| AI Assistant | `/assistant/ask` | Ask travel questions |
| AI Agent | `/agent/ask` | Natural-language flight search |
| Application | `/health` | Backend/database health check |

Consult `/docs` for the exact request schemas and available operations.

## 10. Testing

The project uses Pytest for automated backend testing.

The test suite covers:

- Application and health endpoints.
- User registration and authentication.
- Flight search.
- Booking operations.
- Payment operations.
- AI assistant responses.
- AI agent responses.
- Input validation and error handling.

Run the complete test suite from the project root:

```bash
python -m pytest -q
```

The project has reached **35 passing automated tests** at the latest recorded test run.

A separate test database, `flight_system_test`, is used by the test configuration to isolate automated tests from the application database.

A Postman collection is included in the `postman/` directory for API validation.

## 11. Security and Reliability

Implemented safeguards include:

- Argon2 password hashing.
- JWT authentication.
- Parameterized SQL queries.
- Input validation using Pydantic.
- Booking and payment ownership checks.
- Database transactions and row locking for booking operations.
- Restricted CORS origin for the local frontend.
- Environment-based secret configuration.
- Controlled AI tool allowlisting and argument validation.
- No autonomous AI booking, payment, or cancellation actions.
- Isolated automated test database.

## 12. Project Limitations

- Flight information is sample project data, not live airline schedules.
- No external airline reservation API is integrated.
- Payments are simulated; no real payment gateway is connected.
- The AI assistant answers from the available knowledge base and cannot guarantee current airline-specific policies.
- The AI agent is limited to its explicitly permitted tools.
- Passenger records do not currently have an authenticated-user ownership relationship; passenger ID validation should not be interpreted as passenger-record ownership verification.
- Local AI generation depends on Ollama and the available system hardware.
- Cloud deployment is not yet implemented.

## 13. Future Enhancements

- Deployment using eligible free or student Azure resources.
- Expanded travel knowledge base.
- Improved retrieval evaluation and answer-quality monitoring.
- Additional flight-search capabilities.
- Enhanced frontend experience.
- More automated integration and security tests.
- Expanded documentation and architecture diagrams.

## 14. Developer

**Project:** AI-Powered Smart Flight Reservation and Travel Intelligence Platform

**GitHub:** https://github.com/lubnat-git

---

This project demonstrates practical Python backend development, REST API design, database integration, secure application workflows, automated testing, Retrieval-Augmented Generation, and controlled Agentic AI integration.
