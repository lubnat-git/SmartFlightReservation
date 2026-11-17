from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database import engine
from app.schemas import UserRegister,UserLogin
from app.security import hash_password, verify_password, create_access_token, get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# API: Register a new user
@router.post("/register")
def register_user(user: UserRegister):

    try:
        # Convert normal password into secure hash
        hashed_password = hash_password(user.password)

        # Save user details in MySQL
        query = text("""
            INSERT INTO users (
                full_name,
                email,
                password_hash
            )
            VALUES (
                :full_name,
                :email,
                :password_hash
            )
        """)

        with engine.begin() as connection:

            result = connection.execute(
                query,
                {
                    "full_name": user.full_name,
                    "email": user.email,
                    "password_hash": hashed_password
                }
            )

            new_user_id = result.lastrowid

        return {
            "message": "User registered successfully!",
            "user_id": new_user_id,
            "full_name": user.full_name,
            "email": user.email
        }

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# API: Login an existing user
@router.post("/login")
def login_user(user: UserLogin):

    # Find user using email
    query = text("""
        SELECT user_id, full_name, email, password_hash
        FROM users
        WHERE email = :email
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"email": user.email}
        )

        existing_user = result.fetchone()

    # Check whether user exists
    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify entered password
    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        {"sub": str(existing_user.user_id)}
    )

    return {
        "message": "Login successful!",
        "user_id": existing_user.user_id,
        "full_name": existing_user.full_name,
        "email": existing_user.email,
        "access_token": access_token,
        "token_type": "bearer"
    }

# API: Get details of the currently logged-in user
@router.get("/me")
def get_my_profile(
    current_user: dict = Depends(get_current_user)
):

    query = text("""
        SELECT user_id, full_name, email
        FROM users
        WHERE user_id = :user_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"user_id": current_user["user_id"]}
        )

        user = result.fetchone()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Authenticated user profile",
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email
    }