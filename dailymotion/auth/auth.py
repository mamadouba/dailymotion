import jwt
import time
import uuid
from typing import Optional
from fastapi import Request, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from rick_morty.settings import settings


def sign_jwt(**data: dict) -> dict:
    payload = {
        "email": data.get("email"),
        "expires": time.time() + int(settings.jwt_duration),
        "tuid": str(uuid.uuid4()),
    }
    token = jwt.encode(payload, settings.jwt_secret, settings.jwt_algorithm)
    return dict(access_token=token)


def verify_jwt(token: str) -> dict:
    payload = jwt.decode(
        token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
    )
    return payload


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not credentials.scheme.lower() == "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        try:
            payload = verify_jwt(credentials.credentials)
        except Exception:
            raise HTTPException(status_code=401, detail="Token is not valid.")
        if payload["expires"] < time.time():
            raise HTTPException(status_code=401, detail="Token has expired.")
        from rick_morty.main import revoked_tokens

        if payload["tuid"] in revoked_tokens:
            raise HTTPException(status_code=401, detail="Token has been revoked.")
        request.state.user = payload


def authorize(authorization: Optional[str] = Header(None)) -> dict:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    scheme, token = authorization.split()
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
    try:
        payload = verify_jwt(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Token is not valid.")
    if payload["expires"] < time.time():
        raise HTTPException(status_code=401, detail="Token has expired.")
    from rick_morty.main import revoked_tokens

    if payload["tuid"] in revoked_tokens:
        raise HTTPException(status_code=401, detail="Token has been revoked.")
    return payload
