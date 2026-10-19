import time
import jwt
from security import JWT_SECRET, JWT_ALGORITHM

expired_payload = {
    "sub": "4",
    "exp": int(time.time()) - 60
}

token = jwt.encode(
    expired_payload,
    JWT_SECRET,
    algorithm=JWT_ALGORITHM
)

print(token)