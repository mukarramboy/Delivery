from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_, and_
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
        product_id=order.product_id
    )

    new_order.user = db_user

    session.add(new_order)
    session.commit()
    session.refresh(new_order)  
    data = {
        "success": True,
        "message": "Order created successfully",
        "order_id": new_order.id,
        "quantity": new_order.quantity,
        "status": new_order.status
        }

    return jsonable_encoder(data)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_orders(Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    curent_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == curent_user).first()
    if db_user.is_active:
        orders = session.query(Order).filter(Order.user_id == db_user.id).all()
        data = [{
            "order_id": order.id,
            "quantity": order.quantity,
            "status": order.status,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            }
        } for order in orders]

        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order_by_id(order_id: int, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    curent_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == curent_user).first()
    if db_user.is_staff:
        order = session.query(Order).filter((Order.id == order_id)).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        data = {
            "id": order.id,
            "quantity": order.quantity,
            "status": order.status,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            }
        }
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")
    
@router.get("/{order_id}/detail", status_code=status.HTTP_200_OK)
async def get_order_detail(order_id: int, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    current_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == current_user).first()
    if db_user.is_active:
        order = session.query(Order).filter(Order.id == order_id, Order.user_id == db_user.id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        data = {
            "order_id": order.id,
            "quantity": order.quantity,
            "status": order.status,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email
            }
        }
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")

@router.get("/list", status_code=status.HTTP_200_OK)
async def get_order_list(Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    curent_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == curent_user).first()

    if db_user.is_staff:
        orders = session.query(Order).all()
        data = [{
            "order_id": order.id,
            "quantity": order.quantity,
            "status": order.status
        } for order in orders]

        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")

    
@router.patch("/{order_id}/status", status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, status_update: OrderStatusModel, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    curent_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == curent_user).first()

    if not db_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")
    
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    order.status = status_update.status
    session.commit()
    session.refresh(order)

    data = {
        "success": True,
        "message": "Order status updated successfully",
        "order_id": order.id,
        "new_status": order.status
    }

    return jsonable_encoder(data)

@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
async def delete_order(order_id: int, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    curent_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == curent_user).first()

    if not db_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")
    
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    if order.status != 'PENDING':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only orders with 'PENDING' status can be deleted")
    
    session.delete(order)
    session.commit()

    data = {
        "success": True,
        "message": "Order deleted successfully",
        "order_id": order_id
    }

    return jsonable_encoder(data)