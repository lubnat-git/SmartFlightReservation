from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text

from app.database import engine
from app.schemas import BookingCreate
from app.security import get_current_user


router = APIRouter(
    prefix="/bookings",
    tags=["Flight Bookings"]
)

# API: View logged-in user's booking history
@router.get("/my")
def get_my_bookings(
    current_user: dict = Depends(get_current_user)
):

    try:
        query = text("""
            SELECT
                b.booking_id,
                b.booking_date,
                b.seat_number,
                b.status,
                f.flight_number,
                f.airline_name,
                f.departure_time,
                f.arrival_time,
                a1.city AS source_city,
                a2.city AS destination_city,
                p.full_name AS passenger_name

            FROM bookings b

            JOIN flights f
                ON b.flight_id = f.flight_id

            JOIN airports a1
                ON f.source_airport = a1.airport_id

            JOIN airports a2
                ON f.destination_airport = a2.airport_id

            JOIN passengers p
                ON b.passenger_id = p.passenger_id

            WHERE b.user_id = :user_id

            ORDER BY b.booking_id DESC
        """)

        with engine.connect() as connection:

            result = connection.execute(
                query,
                {"user_id": current_user["user_id"]}
            )

            bookings = [
                dict(row._mapping)
                for row in result
            ]

        return {
            "total_bookings": len(bookings),
            "bookings": bookings
        }

    except Exception as e:

        print("Booking history error:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve booking history"
        )

# API: Book a flight
@router.post("/")
def create_booking(
    booking: BookingCreate,
    current_user: dict = Depends(get_current_user)
):

    try:

        with engine.begin() as connection:

            # Step 1: Find and lock the selected flight
            flight_query = text("""
                SELECT flight_id, seats_availaible
                FROM flights
                WHERE flight_id = :flight_id
                FOR UPDATE
            """)

            flight = connection.execute(
                flight_query,
                {"flight_id": booking.flight_id}
            ).fetchone()

            if flight is None:
                raise HTTPException(
                    status_code=404,
                    detail="Flight not found"
                )

            # Step 2: Check available seats
            if flight.seats_availaible <= 0:
                raise HTTPException(
                    status_code=409,
                    detail="No seats available for this flight"
                )

            # Step 3: Check whether passenger exists
            passenger_query = text("""
                SELECT passenger_id
                FROM passengers
                WHERE passenger_id = :passenger_id
            """)

            passenger = connection.execute(
                passenger_query,
                {"passenger_id": booking.passenger_id}
            ).fetchone()

            if passenger is None:
                raise HTTPException(
                    status_code=404,
                    detail="Passenger not found"
                )

            # Step 4: Find already occupied seats
            occupied_query = text("""
                SELECT seat_number
                FROM bookings
                WHERE flight_id = :flight_id
                AND LOWER(status) <> 'cancelled'
            """)

            occupied_result = connection.execute(
                occupied_query,
                {"flight_id": booking.flight_id}
            )

            occupied_seats = {
                row.seat_number
                for row in occupied_result
            }

            # Step 5: Find the first free seat
            seat_number = None

            for row in range(1, 31):

                for column in ["A", "B", "C", "D", "E", "F"]:

                    candidate = f"{row:02d}{column}"

                    if candidate not in occupied_seats:
                        seat_number = candidate
                        break

                if seat_number is not None:
                    break

            if seat_number is None:
                raise HTTPException(
                    status_code=409,
                    detail="No physical seats available"
                )

            # Step 6: Insert the booking
            insert_query = text("""
                INSERT INTO bookings (
                    flight_id,
                    passenger_id,
                    user_id,
                    seat_number
                )
                VALUES (
                    :flight_id,
                    :passenger_id,
                    :user_id,
                    :seat_number
                )
            """)

            result = connection.execute(
                insert_query,
                {
                    "flight_id": booking.flight_id,
                    "passenger_id": booking.passenger_id,
                    "user_id": current_user["user_id"],
                    "seat_number": seat_number
                }
            )

            new_booking_id = result.lastrowid

            # Step 7: Reduce available seats by one
            update_query = text("""
                UPDATE flights
                SET seats_availaible = seats_availaible - 1
                WHERE flight_id = :flight_id
            """)

            connection.execute(
                update_query,
                {"flight_id": booking.flight_id}
            )

        # Step 8: Return booking details
        return {
            "message": "Flight booked successfully!",
            "booking_id": new_booking_id,
            "flight_id": booking.flight_id,
            "passenger_id": booking.passenger_id,
            "seat_number": seat_number,
            "user_id": current_user["user_id"],
            "remaining_seats": flight.seats_availaible - 1
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Booking error:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to create booking"
        )

# API: Cancel a booking
@router.put("/cancel/{booking_id}")
def cancel_booking(
    booking_id: int,
    current_user: dict = Depends(get_current_user)
):

    try:
        with engine.begin() as connection:

            # Step 1: Find the user's booking and lock it
            booking_query = text("""
                SELECT booking_id, flight_id, status
                FROM bookings
                WHERE booking_id = :booking_id
                AND user_id = :user_id
                FOR UPDATE
            """)

            booking = connection.execute(
                booking_query,
                {
                    "booking_id": booking_id,
                    "user_id": current_user["user_id"]
                }
            ).fetchone()

            if booking is None:
                raise HTTPException(
                    status_code=404,
                    detail="Booking not found"
                )

            # Step 2: Check whether already cancelled
            if booking.status.lower() == "cancelled":
                raise HTTPException(
                    status_code=400,
                    detail="Booking is already cancelled"
                )

            # Step 3: Update booking status
            cancel_query = text("""
                UPDATE bookings
                SET status = 'cancelled'
                WHERE booking_id = :booking_id
            """)

            connection.execute(
                cancel_query,
                {"booking_id": booking_id}
            )

            # Step 4: Restore one available seat
            seat_query = text("""
                UPDATE flights
                SET seats_availaible = LEAST(
                    seats_availaible + 1,
                    total_seats
                )
                WHERE flight_id = :flight_id
            """)

            connection.execute(
                seat_query,
                {"flight_id": booking.flight_id}
            )

        return {
            "message": "Booking cancelled successfully!",
            "booking_id": booking_id,
            "flight_id": booking.flight_id,
            "status": "cancelled"
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Cancellation error:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to cancel booking"
        )