import time
import bcrypt
import random
from dailymotion.models.users import UserActivate
from dailymotion.repositories import Repository
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from dailymotion.models import UserCreate, UserActivate
from dailymotion.dependancies import get_repository, get_redis, get_smtp
from dailymotion.settings import settings

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201)
async def create_user(
    data: UserCreate,
    repository=Depends(get_repository),
    redis=Depends(get_redis),
    smtp=Depends(get_smtp),
):
    if repository.find_user(f"email={data.email}"):
        return JSONResponse(
            status_code=409, content={"detail": "Email address already used"}
        )
    payload = data.dict()
    password = payload.pop("password")
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    payload["password_hash"] = password_hash

    try:
        user = repository.create_user(**payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    activation_code = "".join([str(random.randint(0, 10)) for _ in range(4)])
    expires = time.time() + settings.user_activation_code_expires
    redis.set(f"activation_codes/{data.email}", f"{activation_code},{expires}")

    body = """
    Hello,

    We've recieved your registration. {0} is your activation code.
    This code has a validity of {1} minutes
    
    Thank you
    """.format(
        activation_code, settings.user_activation_code_validity
    )
    smtp.sendmail(data.email, "Activation code", body)
    return {
        "message": "Your activation code has been sent to the email you have provided"
    }


@router.get("/", status_code=200)
async def get_users(repository = Depends(get_repository)):
    try:
        users = repository.get_users()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return users


@router.post("/activate", status_code=200)
async def create_user(
    data: UserActivate, repository=Depends(get_repository), redis=Depends(get_redis), smtp=Depends(get_smtp)
):
    result = redis.get(f"activation_codes/{data.email}")
    if result is None:
        raise HTTPException(
            status_code=403, detail=f"No activation code for {data.email}"
        )
    code, expires = result.decode("utf-8").split(",")
    if code != data.code:
        raise HTTPException(status_code=403, detail=f"Invalid activation code")
    if time.time() > float(expires):
        raise HTTPException(status_code=403, detail=f"Activation code expired")

    user = repository.find_user(f"email={data.email}")
    if user is None:
        raise HTTPException(status_code=403, detail=f"User '{data.email}' not found")

    try:
        updates = {"status": "active"}
        user = repository.update_user(user.get("id"), **updates)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    body = """
    Hello,

    Your account is successfully activated.
    
    Thank you
    """
    smtp.sendmail(data.email, "Activation succeeded", body)
    return user