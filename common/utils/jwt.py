from datetime import datetime, timedelta

import jwt

from django.conf import settings


def jwt_encode(payload: dict, timeout: int = 60) -> str:
    payload.update({
        "jwt_expiry_ts": datetime.now().timestamp() + timeout
    })
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def jwt_decode(token: str) -> dict:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    expiry = payload.pop("jwt_expiry_ts")
    if expiry >= datetime.now().timestamp():
        return payload
