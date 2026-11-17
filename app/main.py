from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import engine
from app.routes.flights import router as flights_router
from app.routes.auth import router as auth_router
from app.routes.bookings import router as bookings_router
from app.routes.payments import router as payments_router

app = FastAPI(
    title="Smart Flight Reservation System",
    description="A flight booking and reservation management API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Smart Flight Reservation System!",
        "database": "MySQL connected"
    }


@app.get("/health")
def health_check():

    try:
        with engine.connect():
            return {
                "status": "Healthy",
                "database": "Connected"
            }

    except Exception:
        return {
            "status": "Unhealthy",
            "database": "Disconnected"
        }


app.include_router(flights_router)
app.include_router(auth_router)
app.include_router(bookings_router)
app.include_router(payments_router)