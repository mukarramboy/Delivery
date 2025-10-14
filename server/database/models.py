from config import Base
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
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    status = Column(ChoiceType([
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ]), default='pending')

    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order(product_name={self.product_name}, quantity={self.quantity}, status={self.status})>"