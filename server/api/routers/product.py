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


@router.get("/", status_code=status.HTTP_200_OK)
async def get_products(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    products = session.query(Product).all()

    data = [{
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "in_stock": product.in_stock
    } for product in products]
    
    return jsonable_encoder(data)


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "in_stock": product.in_stock
    }

    return jsonable_encoder(data)

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    current_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == current_user).first()
    if not db_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    session.delete(product)
    session.commit()

    data = {
        "success": True,
        "message": "Product deleted successfully"
    }

    return jsonable_encoder(data, status_code=status.HTTP_200_OK)


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    current_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == current_user).first()
    if not db_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    
    db_product = session.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    update_product = product.model_dump(exclude_unset=True)
    for key, value in update_product.items():
        setattr(db_product, key, value)

    session.commit()
    session.refresh(db_product)

    data = {
        "success": True,
        "message": "Product updated successfully",
        "product": {
            "id": db_product.id,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "in_stock": db_product.in_stock
        }
    }

    return jsonable_encoder(data)