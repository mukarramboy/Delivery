from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.order_schema import OrderModel, OrderStatusModel
from database.config import session, engine
from database.models import User, Order
from fastapi_jwt_auth2 import AuthJWT


router = APIRouter(
    prefix="/orders",
)

session = session(bind=engine)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    current_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == current_user).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_order = Order(
        quantity=order.quantity,
        status=order.status,
        user_id=db_user.id,
    )
    new_order.user = db_user

    session.add(new_order)
    session.commit()
    session.refresh(new_order)  
    return jsonable_encoder(new_order)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders(Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    curent_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == curent_user).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    orders = session.query(Order).filter(Order.user_id == db_user.id).all()
    return jsonable_encoder(orders)
