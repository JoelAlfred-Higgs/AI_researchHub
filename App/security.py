
from pwdlib import PasswordHash
import os
import jwt

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET_KEY")

if not JWT_SECRET:
    raise RuntimeError("Jwt_secret key is not defined")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(user_id:int): #creates a jwt token for a User
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
    "sub" : str(user_id),
    "exp" : expire
   }   
    return jwt.encode(payload,key = JWT_SECRET, algorithm = JWT_ALGORITHM) 


password_hasher = PasswordHash.recommended()

def hash_password(password:str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str,hashed_password :str) -> bool:
    return password_hasher.verify(password,hashed_password)
    


