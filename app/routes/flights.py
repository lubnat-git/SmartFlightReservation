from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.database import engine

router = APIRouter(
    tags=["Flights and Airports"]
)


# API 1: Get all airports
@router.get("/airports")
def get_airports():

    try:
        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT * FROM airports")
            )

            airports = [
                dict(row._mapping)
                for row in result
            ]

            return {
                "total_airports": len(airports),
                "airports": airports
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@router.get("/flights")
def get_all_flights():

    try:
        query = text("""
            SELECT
                f.flight_id,
                f.airline_name,
                f.flight_number,
                f.departure_time,
                f.arrival_time,
                f.seats_availaible AS seats_available,
                f.price,
                a1.city AS source_city,
                a2.city AS destination_city
            FROM flights f
            JOIN airports a1
                ON f.source_airport = a1.airport_id
            JOIN airports a2
                ON f.destination_airport = a2.airport_id
            ORDER BY f.departure_time
        """)

        with engine.connect() as connection:

            result = connection.execute(query)

            flights = [
                dict(row._mapping)
                for row in result
            ]

            return {
                "total_flights": len(flights),
                "flights": flights
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/search")
def search_flights(source_city: str, destination_city: str):

    try:
        query = text("""
            SELECT
                f.flight_id,
                f.airline_name,
                f.flight_number,
                f.departure_time,
                f.arrival_time,
                f.seats_availaible AS seats_available,
                f.price,
                a1.city AS source_city,
                a2.city AS destination_city
            FROM flights f
            JOIN airports a1
                ON f.source_airport = a1.airport_id
            JOIN airports a2
                ON f.destination_airport = a2.airport_id
            WHERE LOWER(a1.city) = LOWER(:source_city)
            AND LOWER(a2.city) = LOWER(:destination_city)
            AND f.seats_availaible > 0
            ORDER BY f.departure_time
        """)

        with engine.connect() as connection:

            result = connection.execute(
                query,
                {
                    "source_city": source_city,
                    "destination_city": destination_city
                }
            )

            flights = [
                dict(row._mapping)
                for row in result
            ]

            return {
                "total_flights": len(flights),
                "flights": flights
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )