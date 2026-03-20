from fastapi import FastAPI, Response, Cookie
from itsdangerous import TimestampSigner, BadSignature
import uuid
import time

app = FastAPI()

SECRET_KEY = "super_secret_key"
signer = TimestampSigner(SECRET_KEY)

# "база"
fake_user = {
    "username": "user123",
    "password": "password123"
}

SESSION_LIFETIME = 300  # 5 минут
REFRESH_THRESHOLD = 180  # 3 минуты

@app.post("/login")
def login(response: Response, username: str, password: str):
    if username != fake_user["username"] or password != fake_user["password"]:
        response.status_code = 401
        return {"message": "Unauthorized"}

    user_id = str(uuid.uuid4())
    timestamp = int(time.time())

    data = f"{user_id}.{timestamp}"
    signed_data = signer.sign(data.encode()).decode()

    response.set_cookie(
        key="session_token",
        value=signed_data,
        httponly=True,
        max_age=SESSION_LIFETIME
    )

    return {"message": "Logged in"}

@app.get("/profile")
def profile(response: Response, session_token: str = Cookie(default=None)):
    if not session_token:
        response.status_code = 401
        return {"message": "Unauthorized"}

    try:
        unsigned = signer.unsign(session_token.encode()).decode()
    except BadSignature:
        response.status_code = 401
        return {"message": "Invalid session"}

    try:
        user_id, timestamp = unsigned.split(".")
        timestamp = int(timestamp)
    except:
        response.status_code = 401
        return {"message": "Invalid session"}

    current_time = int(time.time())
    diff = current_time - timestamp

    if diff > SESSION_LIFETIME:
        response.status_code = 401
        return {"message": "Session expired"}

    if REFRESH_THRESHOLD <= diff <= SESSION_LIFETIME:
        new_timestamp = current_time
        new_data = f"{user_id}.{new_timestamp}"
        new_signed = signer.sign(new_data.encode()).decode()

        response.set_cookie(
            key="session_token",
            value=new_signed,
            httponly=True,
            max_age=SESSION_LIFETIME
        )

    return {
        "user_id": user_id,
        "status": "active session"
    }