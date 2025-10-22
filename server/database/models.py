from .config import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_staff = Column(Boolean, default=False)  # 0 for regular user, 1 for staff
    is_active = Column(Boolean, default=True)  # 0 for inactive, 1 for active

    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
    

class Order(Base):
    ORDER_STATUSES = (
        ('PENDING', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('DELIVERED', 'delivered'),  
    )

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    status = Column(ChoiceType(ORDER_STATUSES), default='PENDING')
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="orders")
    

    def __repr__(self):
        return f"<Order(product_name={self.product.name}, quantity={self.quantity}, status={self.status})>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=0)
    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price}, stock={self.stock})>"