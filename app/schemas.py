from pydantic import BaseModel, Field


# User registration details
class UserRegister(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: str = Field(
        min_length=5,
        max_length=255
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )
# User login details
class UserLogin(BaseModel):

    email: str

    password: str = Field(
        min_length=8,
        max_length=128
    )

# Flight booking details
class BookingCreate(BaseModel):

    flight_id: int = Field(
        gt=0
    )

    passenger_id: int = Field(
        gt=0
    )

# Payment details
class PaymentCreate(BaseModel):

    booking_id: int = Field(
        gt=0
    )

    mode: str = Field(
        min_length=2,
        max_length=20
    )