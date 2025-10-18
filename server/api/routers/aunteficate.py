from fastapi import APIRouter, status, Depends
from schemas.user_schema import SignUpModel, LoginModel
from database.config import session, engine
from database.models import User
from fastapi.exceptions import HTTPException
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT



router = APIRouter(
    prefix="/auth",
)

session = session(bind=engine)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
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
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(or_(User.email == user.username_or_email, User.username == user.username_or_email)).first()
    
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.id)
        refresh_token = Authorize.create_refresh_token(subject=db_user.id)
        return {"message": "Login successful", "data":{
            "refresh_token": refresh_token,
            "access_token": access_token

        }}      
    

@router.get("/me")
async def get_me():
    return {"message": "User information"}