
from pydantic import BaseModel, Field, EmailStr, field_validator


# User registration details
class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Full name must contain at least 2 non-space characters.")
        return value


# User login details
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


# Flight booking details
class BookingCreate(BaseModel):
    flight_id: int = Field(gt=0)
    passenger_id: int = Field(gt=0)


# Payment details
class PaymentCreate(BaseModel):
    booking_id: int = Field(gt=0)
    mode: str = Field(min_length=2, max_length=20)


# AI assistant request
class AssistantAsk(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Question cannot contain only whitespace.")
        return value


# AI assistant response
class AssistantResponse(BaseModel):
    answer: str
    sources: list[str]


# AI agent request
class AgentAsk(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Question cannot contain only whitespace.")
        return value


# AI agent response
class AgentResponse(BaseModel):
    answer: str
    flights: list[dict]
    tools_used: list[str]
