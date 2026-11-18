import uuid
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.database import engine

client = TestClient(app)


@pytest.fixture
def booking_context():

    # Create a unique test user
    email = f"booking_{uuid.uuid4().hex[:10]}@example.com"
    password = "TestPass123"

    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Booking Test User",
            "email": email,
            "password": password
        }
    )

    assert register_response.status_code == 200

    user_id = register_response.json()["user_id"]

    # Log in and obtain JWT token
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Prepare test airports, flight and passenger
    passport = f"PYT{uuid.uuid4().hex[:12]}"

    with engine.begin() as connection:

        connection.execute(
            text("""
                INSERT IGNORE INTO airports
                (airport_name, city, country)
                VALUES
                ('Pytest Source Airport', 'PytestSourceCity', 'India'),
                ('Pytest Destination Airport',
                 'PytestDestinationCity', 'India')
            """)
        )

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

        flight_id = connection.execute(
            text("""
                SELECT flight_id
                FROM flights
                WHERE flight_number = 'PYT001'
            """)
        ).scalar_one()

        passenger_result = connection.execute(
            text("""
                INSERT INTO passengers (
                    full_name,
                    gender,
                    nationality,
                    passport_number,
                    contact_number
                )
                VALUES (
                    'Pytest Passenger',
                    'male',
                    'Indian',
                    :passport,
                    '9999999999'
                )
            """),
            {"passport": passport}
        )

        passenger_id = passenger_result.lastrowid

    # Provide test information to individual tests
    yield {
        "user_id": user_id,
        "flight_id": flight_id,
        "passenger_id": passenger_id,
        "headers": headers
    }

    # Clean up test records after each test
    with engine.begin() as connection:

        bookings = connection.execute(
            text("""
                SELECT booking_id, flight_id, status
                FROM bookings
                WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchall()

        for booking in bookings:

            # Restore seats for bookings that were not cancelled
            if booking.status.lower() != "cancelled":
                connection.execute(
                    text("""
                        UPDATE flights
                        SET seats_availaible = LEAST(
                            seats_availaible + 1,
                            total_seats
                        )
                        WHERE flight_id = :flight_id
                    """),
                    {"flight_id": booking.flight_id}
                )

        connection.execute(
            text("""
                DELETE FROM payments
                WHERE booking_id IN (
                    SELECT booking_id
                    FROM bookings
                    WHERE user_id = :user_id
                )
            """),
            {"user_id": user_id}
        )

        connection.execute(
            text("""
                DELETE FROM bookings
                WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        )

        connection.execute(
            text("""
                DELETE FROM passengers
                WHERE passenger_id = :passenger_id
            """),
            {"passenger_id": passenger_id}
        )

        connection.execute(
            text("""
                DELETE FROM users
                WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        )


def test_create_booking_successfully(booking_context):

    response = client.post(
        "/bookings/",
        json={
            "flight_id": booking_context["flight_id"],
            "passenger_id": booking_context["passenger_id"]
        },
        headers=booking_context["headers"]
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Flight booked successfully!"
    assert response.json()["booking_id"] > 0


def test_booking_invalid_flight(booking_context):

    response = client.post(
        "/bookings/",
        json={
            "flight_id": 2147483647,
            "passenger_id": booking_context["passenger_id"]
        },
        headers=booking_context["headers"]
    )

    assert response.status_code == 404


def test_booking_invalid_passenger(booking_context):

    response = client.post(
        "/bookings/",
        json={
            "flight_id": booking_context["flight_id"],
            "passenger_id": 2147483647
        },
        headers=booking_context["headers"]
    )

    assert response.status_code == 404


def test_booking_without_authentication(booking_context):

    response = client.post(
        "/bookings/",
        json={
            "flight_id": booking_context["flight_id"],
            "passenger_id": booking_context["passenger_id"]
        }
    )

    assert response.status_code == 401


def test_view_booking_history(booking_context):

    client.post(
        "/bookings/",
        json={
            "flight_id": booking_context["flight_id"],
            "passenger_id": booking_context["passenger_id"]
        },
        headers=booking_context["headers"]
    )

    response = client.get(
        "/bookings/my",
        headers=booking_context["headers"]
    )

    assert response.status_code == 200
    assert response.json()["total_bookings"] >= 1


def test_cancel_booking_successfully(booking_context):

    booking_response = client.post(
        "/bookings/",
        json={
            "flight_id": booking_context["flight_id"],
            "passenger_id": booking_context["passenger_id"]
        },
        headers=booking_context["headers"]
    )

    booking_id = booking_response.json()["booking_id"]

    response = client.put(
        f"/bookings/cancel/{booking_id}",
        headers=booking_context["headers"]
    )

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


def test_prevent_duplicate_cancellation(booking_context):

    booking_response = client.post(
        "/bookings/",
        json={
            "flight_id": booking_context["flight_id"],
            "passenger_id": booking_context["passenger_id"]
        },
        headers=booking_context["headers"]
    )

    booking_id = booking_response.json()["booking_id"]

    # First cancellation
    client.put(
        f"/bookings/cancel/{booking_id}",
        headers=booking_context["headers"]
    )

    # Second cancellation should be rejected
    response = client.put(
        f"/bookings/cancel/{booking_id}",
        headers=booking_context["headers"]
    )

    assert response.status_code == 400