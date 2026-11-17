from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text

from app.database import engine
from app.schemas import PaymentCreate
from app.security import get_current_user


router = APIRouter(
    prefix="/payments",
    tags=["Flight Payments"]
)


# API: Make a simulated flight payment
@router.post("/")
def make_payment(
    payment: PaymentCreate,
    current_user: dict = Depends(get_current_user)
):

    try:

        # Step 1: Validate payment method
        allowed_modes = [
            "upi",
            "card",
            "netbanking",
            "cash"
        ]

        payment_mode = payment.mode.lower()

        if payment_mode not in allowed_modes:
            raise HTTPException(
                status_code=400,
                detail="Invalid payment method"
            )

        with engine.begin() as connection:

            # Step 2: Find booking and check ownership
            booking_query = text("""
                SELECT
                    b.booking_id,
                    b.flight_id,
                    b.status,
                    b.user_id,
                    f.price
                FROM bookings b
                JOIN flights f
                    ON b.flight_id = f.flight_id
                WHERE b.booking_id = :booking_id
                AND b.user_id = :user_id
                FOR UPDATE
            """)

            booking = connection.execute(
                booking_query,
                {
                    "booking_id": payment.booking_id,
                    "user_id": current_user["user_id"]
                }
            ).fetchone()

            if booking is None:
                raise HTTPException(
                    status_code=404,
                    detail="Booking not found"
                )

            # Step 3: Check booking status
            if booking.status.lower() == "cancelled":
                raise HTTPException(
                    status_code=400,
                    detail="Cannot pay for a cancelled booking"
                )

            # Step 4: Check whether payment already exists
            existing_payment_query = text("""
                SELECT payment_id, status
                FROM payments
                WHERE booking_id = :booking_id
                ORDER BY payment_id DESC
                LIMIT 1
                FOR UPDATE
            """)

            existing_payment = connection.execute(
                existing_payment_query,
                {"booking_id": payment.booking_id}
            ).fetchone()

            if existing_payment is not None:

                if existing_payment.status.lower() == "paid":
                    raise HTTPException(
                        status_code=409,
                        detail="Payment already completed"
                    )

                # Update an earlier pending or failed payment
                update_payment_query = text("""
                    UPDATE payments
                    SET
                        amount = :amount,
                        mode = :mode,
                        status = 'paid',
                        payment_date = CURRENT_DATE
                    WHERE payment_id = :payment_id
                """)

                connection.execute(
                    update_payment_query,
                    {
                        "amount": booking.price,
                        "mode": payment_mode,
                        "payment_id": existing_payment.payment_id
                    }
                )

                payment_id = existing_payment.payment_id

            else:

                # Step 5: Insert a new payment record
                insert_payment_query = text("""
                    INSERT INTO payments (
                        booking_id,
                        amount,
                        mode,
                        status
                    )
                    VALUES (
                        :booking_id,
                        :amount,
                        :mode,
                        'paid'
                    )
                """)

                result = connection.execute(
                    insert_payment_query,
                    {
                        "booking_id": payment.booking_id,
                        "amount": booking.price,
                        "mode": payment_mode
                    }
                )

                payment_id = result.lastrowid

        # Step 6: Return payment details
        return {
            "message": "Payment successful!",
            "payment_id": payment_id,
            "booking_id": payment.booking_id,
            "amount": booking.price,
            "payment_mode": payment_mode,
            "payment_status": "paid",
            "payment_type": "Simulated payment"
        }

    except HTTPException:
        raise

    except Exception as e:

        print("Payment error:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to process payment"
        )