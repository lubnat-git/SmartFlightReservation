import uuid
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.database import engine

client = TestClient(app)


@pytest.fixture
def payment_context():

    # Create a unique user
    email = f"payment_{uuid.uuid4().hex[:10]}@example.com"
    password = "TestPass123"

    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Payment Test User",
            "email": email,
            "password": password
        }
    )

    assert register_response.status_code == 200

    user_id = register_response.json()["user_id"]

    # Login and obtain JWT token
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

    passport = f"PAY{uuid.uuid4().hex[:12]}"

    # Prepare test flight and passenger
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
                    'Payment Test Passenger',
                    'male',
                    'Indian',
                    :passport,
                    '9999999999'
                )
            """),
            {"passport": passport}
        )

        passenger_id = passenger_result.lastrowid

    # Create a booking for this user
    booking_response = client.post(
        "/bookings/",
        json={
            "flight_id": flight_id,
            "passenger_id": passenger_id
        },
        headers=headers
    )

    assert booking_response.status_code == 200

    booking_id = booking_response.json()["booking_id"]

    yield {
        "user_id": user_id,
        "booking_id": booking_id,
        "headers": headers,
        "flight_id": flight_id,
        "passenger_id": passenger_id
    }

    # Clean up test data and restore seats
    with engine.begin() as connection:

        connection.execute(
            text("""
                DELETE FROM payments
                WHERE booking_id = :booking_id
            """),
            {"booking_id": booking_id}
        )

        connection.execute(
            text("""
                SELECT status
                FROM bookings
                WHERE booking_id = :booking_id
            """),
            {"booking_id": booking_id}
        )

        booking_status = connection.execute(
            text("""
                SELECT status
                FROM bookings
                WHERE booking_id = :booking_id
            """),
            {"booking_id": booking_id}
        ).scalar_one_or_none()

        if booking_status is not None and booking_status.lower() != "cancelled":

            connection.execute(
                text("""
                    UPDATE flights
                    SET seats_availaible = LEAST(
                        seats_availaible + 1,
                        total_seats
                    )
                    WHERE flight_id = :flight_id
                """),
                {"flight_id": flight_id}
            )

        connection.execute(
            text("""
                DELETE FROM bookings
                WHERE booking_id = :booking_id
            """),
            {"booking_id": booking_id}
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


def test_successful_payment(payment_context):

    response = client.post(
        "/payments/",
        json={
            "booking_id": payment_context["booking_id"],
            "mode": "upi"
        },
        headers=payment_context["headers"]
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Payment successful!"
    assert response.json()["payment_status"] == "paid"
    assert response.json()["amount"] == 5000


def test_invalid_payment_mode(payment_context):

    response = client.post(
        "/payments/",
        json={
            "booking_id": payment_context["booking_id"],
            "mode": "bitcoin"
        },
        headers=payment_context["headers"]
    )

    assert response.status_code == 400


def test_payment_for_another_users_booking(payment_context):

    # Register another user
    email = f"other_{uuid.uuid4().hex[:10]}@example.com"

    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Another Test User",
            "email": email,
            "password": "TestPass123"
        }
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPass123"
        }
    )

    other_token = login_response.json()["access_token"]

    response = client.post(
        "/payments/",
        json={
            "booking_id": payment_context["booking_id"],
            "mode": "upi"
        },
        headers={
            "Authorization": f"Bearer {other_token}"
        }
    )

    assert response.status_code == 404


def test_payment_for_cancelled_booking(payment_context):

    # Cancel the booking first
    cancel_response = client.put(
        f"/bookings/cancel/{payment_context['booking_id']}",
        headers=payment_context["headers"]
    )

    assert cancel_response.status_code == 200

    response = client.post(
        "/payments/",
        json={
            "booking_id": payment_context["booking_id"],
            "mode": "card"
        },
        headers=payment_context["headers"]
    )

    assert response.status_code == 400


def test_prevent_duplicate_successful_payment(payment_context):

    payment_data = {
        "booking_id": payment_context["booking_id"],
        "mode": "upi"
    }

    # First payment
    first_response = client.post(
        "/payments/",
        json=payment_data,
        headers=payment_context["headers"]
    )

    assert first_response.status_code == 200

    # Second payment should be rejected
    second_response = client.post(
        "/payments/",
        json=payment_data,
        headers=payment_context["headers"]
    )

    assert second_response.status_code == 409


def test_payment_without_authentication(payment_context):

    response = client.post(
        "/payments/",
        json={
            "booking_id": payment_context["booking_id"],
            "mode": "upi"
        }
    )

    assert response.status_code == 401