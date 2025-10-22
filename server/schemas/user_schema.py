from pydantic import BaseModel
from typing import Optional
from datetime import timedelta

class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    
    model_config = {
        "from_attributes": True,  # заменяет orm_mode = True
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "securepassword",
                "is_staff": False,
                "is_active": True
            }
        }
    }
        

class Settings(BaseModel):
    authjwt_secret_key : str = "5ffc4280efac0a3b89f3e014d1b3e373eba3bc15b5ea22bc3c6fff60b6de9d89"


class LoginModel(BaseModel):
    username_or_email: str
    password: str

    model_config = {
        "from_attributes": True,   # заменяет orm_mode=True
        "json_schema_extra": {
            "example": {
                "username_or_email": "johndoe",
                "password": "securepassword",
            }
        }
    }