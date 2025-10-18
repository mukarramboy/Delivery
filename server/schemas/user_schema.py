from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "securepassword",
                "is_staff": False,
                "is_active": True
            }
        }
        

class Settings(BaseModel):
    authjwt_secret_key: str = "ac6c14f448a52ec5316ce95b84460342e4f038a48e3248b32f35ac14459fd4db"


class LoginModel(BaseModel):
    username_or_email: str
    password: str

    class Config:
        orm_mode = True
        json_schema_extra ={
            "example":{
                "username_or_email": "johndoe",
                "password":"securepassword",
            }
        }