from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.user_schema import SignUpModel, LoginModel
from database.config import session, engine
from database.models import User
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth2 import AuthJWT


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
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        data = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        response = {
            "success": True,
            "message": "Login successful",
            "data": data
        }
        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username/email or password")


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(User).filter(User.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        new_access_token = Authorize.create_access_token(subject=current_user)
        response = {
            "access_token": new_access_token
        }
        return jsonable_encoder(response)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    


@router.get("/profile", status_code=status.HTTP_200_OK)
async def profile(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        db_user = session.query(User).filter(User.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        response = {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "is_staff": db_user.is_staff,
            "is_active": db_user.is_active
        }
        return jsonable_encoder(response)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    