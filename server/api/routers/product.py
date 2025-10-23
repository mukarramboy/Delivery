from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth2 import AuthJWT

from database.config import session, engine
from database.models import Product, User
from schemas.product_schema import ProductModel



router = APIRouter(
    prefix="/products",
)

session = session(bind=engine)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    current_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == current_user).first()
    if not db_user or not db_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        in_stock=product.in_stock
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return jsonable_encoder(new_product)