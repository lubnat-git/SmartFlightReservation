import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.database import engine

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def prepare_test_flight_data():

    with engine.begin() as connection:

        # Create test airports if they do not exist
        connection.execute(
            text("""
                INSERT IGNORE INTO airports
                (airport_name, city, country)
                VALUES
                ('Pytest Source Airport', 'PytestSourceCity', 'India'),
                ('Pytest Destination Airport', 'PytestDestinationCity', 'India')
            """)
        )

        # Get airport IDs
        source_id = connection.execute(
            text("""
                SELECT airport_id
                FROM airports
                WHERE city = 'PytestSourceCity'
            """)
        ).scalar_one()

        destination_id = connection.execute(
            text("""
                SELECT airport_id
                FROM airports
                WHERE city = 'PytestDestinationCity'
            """)
        ).scalar_one()

        # Create a test flight if it does not exist
        connection.execute(
            text("""
                INSERT IGNORE INTO flights (
                    airline_name,
                    flight_number,
                    source_airport,
                    destination_airport,
                    departure_time,
                    arrival_time,
                    seats_availaible,
                    price,
                    total_seats
                )
                VALUES (
                    'Pytest Airlines',
                    'PYT001',
                    :source_id,
                    :destination_id,
                    '2027-01-10 10:00:00',
                    '2027-01-10 12:00:00',
                    50,
                    5000,
                    180
                )
            """),
            {
                "source_id": source_id,
                "destination_id": destination_id
            }
        )


def test_get_all_airports():

    response = client.get("/airports")

    assert response.status_code == 200
    assert response.json()["total_airports"] >= 2


def test_get_all_flights():

    response = client.get("/flights")

    assert response.status_code == 200
    assert response.json()["total_flights"] >= 1

    flight_numbers = [
        flight["flight_number"]
        for flight in response.json()["flights"]
    ]

    assert "PYT001" in flight_numbers


def test_search_flights():

    response = client.get(
        "/search",
        params={
            "source_city": "PytestSourceCity",
            "destination_city": "PytestDestinationCity"
        }
    )

    assert response.status_code == 200
    assert response.json()["total_flights"] >= 1
    assert response.json()["flights"][0]["flight_number"] == "PYT001"


def test_search_flights_case_insensitive():

    response = client.get(
        "/search",
        params={
            "source_city": "pytestsourcecity",
            "destination_city": "pytestdestinationcity"
        }
    )

    assert response.status_code == 200
    assert response.json()["total_flights"] >= 1


def test_search_flights_no_matching_route():

    response = client.get(
        "/search",
        params={
            "source_city": "NonexistentCity",
            "destination_city": "AnotherNonexistentCity"
        }
    )

    assert response.status_code == 200
    assert response.json()["total_flights"] == 0