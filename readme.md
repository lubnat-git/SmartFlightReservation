\# ✈️ AI-Powered Smart Flight Reservation System



A web-based flight reservation application built using Python, FastAPI, MySQL, and JavaScript. The project provides essential flight booking functionality, secure user authentication, booking management, and simulated payment processing, with Generative AI and intelligent travel assistance planned as the next development phase.



\---



\## 📌 1. Project Overview



The Smart Flight Reservation System aims to simplify the flight booking process through a centralized web application.



Users can register, log in, search for available flights, reserve seats, make simulated payments, view their booking history, and cancel reservations.



The long-term vision is to integrate Generative AI, Retrieval-Augmented Generation (RAG), and Agentic AI to provide intelligent travel assistance and conversational flight search.



\## 🎯 2. Problem Statement



Traditional flight reservation workflows can involve multiple steps to search for flights, manage reservations, and access travel information.



This project aims to provide a simple and integrated platform that:



\- Simplifies flight searching and reservation.

\- Provides secure user authentication.

\- Prevents unauthorized access to bookings.

\- Manages seat availability during reservations.

\- Supports booking cancellation.

\- Provides simulated payment processing.

\- Creates a foundation for AI-powered travel assistance.



\## 🛠️ 3. Technology Stack



| Category | Technologies |

|---|---|

| Programming Language | Python |

| Backend Framework | FastAPI |

| Database | MySQL 8.0 |

| Database Connectivity | SQLAlchemy, PyMySQL |

| Frontend | HTML, CSS, JavaScript |

| Authentication | JWT |

| Password Security | Argon2 |

| API Documentation | Swagger UI |

| API Testing | Postman (planned) |

| Automated Testing | Pytest (planned) |

| Version Control | Git |

| Code Hosting | GitHub |

| AI Integration | Generative AI / LLM (planned) |

| AI Retrieval | RAG, Embeddings, Vector Search (planned) |

| Cloud Deployment | Microsoft Azure (planned) |



\## ✨ 4. Implemented Features



\### User Authentication

\- User registration.

\- User login.

\- Secure password hashing using Argon2.

\- JWT-based authentication.

\- Protected API endpoints.



\### Flight Management

\- Retrieve available flights.

\- Search flights using source and destination cities.

\- Display airline information.

\- Display departure and arrival details.

\- Display ticket prices and available seats.



\### Booking Management

\- Reserve available flight seats.

\- Automatic seat allocation.

\- Prevent booking when seats are unavailable.

\- User-specific booking history.

\- Cancel existing reservations.

\- Restore seat availability after cancellation.

\- Prevent unauthorized access to another user's booking.



\### Payment Management

\- Simulated payment processing.

\- Supported payment modes:

&#x20; - UPI

&#x20; - Card

&#x20; - Net Banking

&#x20; - Cash

\- Booking ownership validation.

\- Prevent duplicate successful payments.

\- Payment status management.



\*\*Note:\*\* Payments are simulated. No real money is transferred and no external payment gateway is integrated.



\## 🧠 5. Planned AI Capabilities



The following capabilities are part of the next development phase.



\### Generative AI Travel Assistant

A conversational assistant that will help users understand travel-related information and interact with the flight reservation system.



\### Retrieval-Augmented Generation (RAG)

A travel knowledge assistant using:

\- Text embeddings.

\- Vector storage.

\- Semantic search.

\- Context retrieval.

\- LLM-based response generation.



The knowledge base will contain travel FAQs and information about baggage, check-in, cancellation policies, and travel documentation.



\### Agentic AI Flight Search

An intelligent flight-search agent designed to:

\- Understand natural-language flight requests.

\- Extract source and destination information.

\- Call existing flight-search APIs.

\- Compare available flights.

\- Present suitable flight options.



Booking and payment actions will require explicit user confirmation.



\## 🏗️ 6. Project Architecture



The application follows a client-server architecture.



```text

&#x20;                USER

&#x20;                  |

&#x20;                  v

&#x20;         FRONTEND APPLICATION

&#x20;            HTML / CSS / JS

&#x20;                  |

&#x20;                  v

&#x20;            FASTAPI BACKEND

&#x20;                  |

&#x20;       +----------+----------+

&#x20;       |          |          |

&#x20;       v          v          v

&#x20;  Authentication Flights  Bookings

&#x20;       |          |          |

&#x20;       +----------+----------+

&#x20;                  |

&#x20;                  v

&#x20;             MYSQL DATABASE

&#x20;                  |

&#x20;                  v

&#x20;           PAYMENT MODULE

&#x20;           (Simulated)

```



Planned AI integration:



```text

&#x20;            USER QUESTION

&#x20;                  |

&#x20;                  v

&#x20;          AI TRAVEL ASSISTANT

&#x20;                  |

&#x20;                  v

&#x20;           RAG PIPELINE

&#x20;                  |

&#x20;           +------+------+

&#x20;           |             |

&#x20;           v             v

&#x20;       EMBEDDINGS    VECTOR SEARCH

&#x20;           |             |

&#x20;           +------+------+

&#x20;                  |

&#x20;                  v

&#x20;             LLM RESPONSE

```



\## 📁 7. Project Structure



```text

SmartFlightReservation/

│

├── app/

│   ├── \_\_init\_\_.py

│   ├── main.py

│   ├── database.py

│   ├── security.py

│   ├── schemas.py

│   │

│   └── routes/

│       ├── \_\_init\_\_.py

│       ├── auth.py

│       ├── flights.py

│       ├── bookings.py

│       └── payments.py

│

├── frontend/

│   ├── index.html

│   ├── style.css

│   └── script.js

│

├── .gitignore

├── README.md

└── .env

```



\*\*Security note:\*\* The `.env` file contains local configuration and secrets. It is excluded from version control and must never be uploaded to GitHub.



\## ⚙️ 8. Installation and Setup



\### Prerequisites



\- Python 3.12 or later.

\- MySQL 8.0 or later.

\- Git.

\- Visual Studio Code or another code editor.

\- A modern web browser.



\### Step 1: Clone the Repository



```bash

git clone https://github.com/lubnat-git/SmartFlightReservation.git

```



\### Step 2: Navigate to the Project



```bash

cd SmartFlightReservation

```



\### Step 3: Create a Virtual Environment



```bash

python -m venv venv

```



Activate it on Windows:



```powershell

venv\\Scripts\\activate

```



\### Step 4: Install Dependencies



Install the Python packages used by the application:



```bash

pip install fastapi uvicorn sqlalchemy pymysql python-dotenv "pwdlib\[argon2]" PyJWT

```



\### Step 5: Configure Environment Variables



Create a local `.env` file in the project root.



Configure the database connection details and JWT secret using the variable names expected by the application.



Never commit this file or share its secret values.



\### Step 6: Configure MySQL



Create the MySQL database:



```sql

CREATE DATABASE flight\_system;

```



Create and populate the required tables using the database schema for this application.



Ensure that the database connection settings in `.env` match your local MySQL configuration.



\### Step 7: Start the Backend



```bash

uvicorn app.main:app --reload

```



The backend will run at:



```text

http://127.0.0.1:8000

```



\### Step 8: Access API Documentation



Open the following address in your browser:



```text

http://127.0.0.1:8000/docs

```



Swagger UI provides interactive documentation for exploring and testing the API endpoints.



\### Step 9: Start the Frontend



Open the `frontend` folder in Visual Studio Code and launch `index.html` using the Live Server extension.



The frontend is configured for:



```text

http://localhost:5500

```



\## 🔌 9. API Modules



The backend provides the following API modules:



| Module | Functionality |

|---|---|

| Authentication | Registration, login, current user |

| Flights | Flight listing and searching |

| Bookings | Reservation, history, cancellation |

| Payments | Simulated payment processing |



Interactive API documentation is available at `/docs`.



\## 🔐 10. Security Considerations



\- Passwords are hashed using Argon2.

\- JWT tokens protect authenticated endpoints.

\- Booking ownership is validated.

\- Payment ownership is validated.

\- Database queries use parameterized SQL.

\- Environment variables are used for sensitive configuration.

\- Secrets and virtual environments are excluded through `.gitignore`.



\## 🚀 11. Future Enhancements



\- Generative AI travel assistant.

\- RAG-based travel knowledge retrieval.

\- Semantic search using embeddings.

\- Vector database integration.

\- Agentic AI for intelligent flight search.

\- Automated backend testing using Pytest.

\- API testing using Postman.

\- Cloud deployment using eligible Azure resources.

\- Improved documentation and architecture diagrams.



\## ⚠️ 12. Project Limitations



\- Flight schedules and airline details currently represent sample project data, not live airline schedules.

\- No external airline booking API is connected.

\- Payments are simulated.

\- AI assistant and agentic capabilities are planned, not yet implemented.

\- Cloud deployment is planned.



\## 👩‍💻 13. Developer



\*\*Project:\*\* AI-Powered Smart Flight Reservation System



\*\*GitHub:\*\* https://github.com/lubnat-git



\---



⭐ This project is being developed as a portfolio project to demonstrate backend development, database integration, secure API design, web application development, and practical AI integration.



