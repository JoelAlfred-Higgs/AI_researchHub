# ==============================================================================
# Authentication & Dependency Injection
# ==============================================================================
# This file defines FastAPI "dependencies" - reusable functions that run before
# your route handlers (endpoints) to verify user authentication and provide
# needed resources (like the current user and database session).
# ==============================================================================

# these comments are for learning purposes
# here we are defining a dependency function called get_current_user
# this function will be called before every protected route handler
# the purpose of this function is to extract the JWT token from the request header
# and verify that the token is valid
# if the token is valid, the function will return the user object
# if the token is invalid, the function will raise an HTTPException

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends,HTTPException
from DataBase import get_db
from security import JWT_ALGORITHM,JWT_SECRET
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models import User


# Set up HTTP Bearer token authentication scheme.
# HTTPBearer looks for the "Authorization: Bearer <token>" header in incoming HTTP requests.
# auto_error=False allows us to handle missing or invalid tokens manually with custom messages.
bearer_schema = HTTPBearer(auto_error=False)

# ------------------------------------------------------------------------------
# Dependency: get_current_user
# ------------------------------------------------------------------------------
# How to use in an API endpoint:
#   @app.get("/profile")
#   def get_profile(current_user: User = Depends(get_current_user)):
#       return {"username": current_user.username}
#
# FastAPI handles dependency injection automatically:
# 1. credentials -> extracts token from "Authorization: Bearer <token>"
# 2. db          -> provides an active SQLAlchemy database session via get_db()
# ------------------------------------------------------------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_schema),
    db: Session = Depends(get_db)
):
    # Step 1: Check if the client provided a Bearer token in the request header
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 2: Decode and verify the JWT token
    try:
        # jwt.decode checks the signature using JWT_SECRET and ensures the token is valid & not expired
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub"))

    except (InvalidTokenError, KeyError, TypeError, ValueError):
        # Triggers if the token signature is invalid, expired, or malformed
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 3: Query the database to find the user with this user_id
    user = db.query(User).filter(User.user_id == user_id).first()

    # Step 4: If no user with that ID exists in the database, reject the request
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 5: Return the authenticated User model object to the route handler
    return user


   
