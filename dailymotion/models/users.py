import re
from pydantic import BaseModel, validator

EMAIL_REGX = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"


def validate_email_address(email):
    regex = re.compile(EMAIL_REGX)
    if not regex.fullmatch(email):
        raise ValueError("Email address not valid")
    return email


class UserCreate(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v):
        return validate_email_address(v)

    @validator("password")
    def vaildate_password(cls, v):
        if not (4 < len(v) < 8):
            raise ValueError("Password must be 8 to 16 characters long")
        if not any([c.isdigit() for c in v]):
            raise ValueError("Password must have at least 6 caracters")
        if not any([c.isupper() for c in v]):
            raise ValueError("Password must contains at least one uppercase")
        if not any([c.islower() for c in v]):
            raise ValueError("Password must contains at least one lowercase")
        if not any([c in v for c in "&!$@"]):
            raise ValueError(
                "Password must contains at least one special caracter: &!$@"
            )
        return v

    class Config:
        schema_extra = {
            "example": {"email": "john.doe@mailhog.local", "password": "Aze123!"}
        }


class UserActivate(BaseModel):
    code: str
    email: str

    @validator("code")
    def validate_code(cls, v):
        if (len(v) != 4) or (not v.isdigit()):
            raise ValueError("Invalid user activation code")
        return v

    @validator("email")
    def validate_email(cls, v):
        return validate_email_address(v)

    class Config:
        schema_extra = {"example": {"email": "john.doe@mailhog.local", "code": "1122"}}
