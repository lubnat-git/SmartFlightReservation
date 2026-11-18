
from sqlalchemy import text

from app.database import engine
from app.routes.flights import get_matching_flights


def search_flights(source_city: str, destination_city: str):
    """Search available flights between two cities."""

    if not source_city.strip() or not destination_city.strip():
        return {
            "success": False,
            "message": "Source and destination cities are required.",
            "flights": []
        }

    try:
        flights = get_matching_flights(
            source_city.strip(),
            destination_city.strip()
        )

        return {
            "success": True,
            "total_flights": len(flights),
            "flights": flights
        }

    except Exception:
        return {
            "success": False,
            "message": "Unable to search flights at the moment.",
            "flights": []
        }


def compare_flights(flights: list):
    """Compare flights by ticket price."""

    if not flights:
        return {
            "success": False,
            "message": "No flights available for comparison.",
            "flights": []
        }

    try:
        sorted_flights = sorted(
            flights,
            key=lambda flight: float(flight["price"])
        )

        return {
            "success": True,
            "total_flights": len(sorted_flights),
            "flights": sorted_flights
        }

    except (KeyError, TypeError, ValueError):
        return {
            "success": False,
            "message": "Unable to compare flight prices.",
            "flights": []
        }


def find_cheapest_flight(flights: list):
    """Find the cheapest flight from matching results."""

    comparison = compare_flights(flights)

    if not comparison["success"]:
        return comparison

    return {
        "success": True,
        "cheapest_flight": comparison["flights"][0]
    }


def check_seat_availability(flight_id: int):
    """Check the remaining seats for a flight."""

    if flight_id <= 0:
        return {
            "success": False,
            "message": "Invalid flight ID."
        }

    try:
        query = text("""
            SELECT seats_availaible
            FROM flights
            WHERE flight_id = :flight_id
        """)

        with engine.connect() as connection:
            result = connection.execute(
                query,
                {"flight_id": flight_id}
            ).fetchone()

        if result is None:
            return {
                "success": False,
                "message": "Flight not found."
            }

        return {
            "success": True,
            "flight_id": flight_id,
            "available_seats": result[0]
        }

    except Exception:
        return {
            "success": False,
            "message": "Unable to check seat availability."
        }
