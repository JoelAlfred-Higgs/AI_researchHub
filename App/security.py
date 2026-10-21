
from pwdlib import PasswordHash
import os
from pathlib import Path
import jwt

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()
load_dotenv(Path(__file__).with_name(".env"))

class ConfigurationError(RuntimeError):
    """Raised when required authentication configuration is missing or invalid."""


def get_jwt_secret() -> str:
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if not jwt_secret:
        raise ConfigurationError("JWT_SECRET_KEY is not configured")
    return jwt_secret


def get_jwt_algorithm() -> str:
    return os.getenv("JWT_ALGORITHM", "HS256")


def get_access_token_expire_minutes() -> int:
    try:
        expires_in = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    except ValueError as exc:
        raise ConfigurationError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer") from exc
    if expires_in <= 0:
        raise ConfigurationError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")
    return expires_in


def validate_security_config():
    get_jwt_secret()
    get_access_token_expire_minutes()

def create_access_token(user_id:int): #creates a jwt token for a User
    expire = datetime.now(timezone.utc) + timedelta(minutes=get_access_token_expire_minutes())

    payload = {
    "sub" : str(user_id),
    "exp" : expire
   }   
    return jwt.encode(payload, key=get_jwt_secret(), algorithm=get_jwt_algorithm())


password_hasher = PasswordHash.recommended()

def hash_password(password:str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str,hashed_password :str) -> bool:
    return password_hasher.verify(password,hashed_password)
    


