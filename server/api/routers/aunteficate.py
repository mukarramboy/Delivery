from fastapi import APIRouter, status
from schemas import SignUpModel
from database.config import session
from database.models import User
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/auth",
)

@router.post("/signup")
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    session.add(new_user)


@router.post("/login")
async def login():
    return {"message": "Login successful"}

@router.get("/me")
async def get_me():
    return {"message": "User information"}