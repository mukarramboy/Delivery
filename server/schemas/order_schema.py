from pydantic import BaseModel
from typing import Optional


class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    status: Optional[str] = "PENDING"
    user_id: Optional[int] = None


    model_config = {
        "from_attributes": True,  # заменяет orm_mode = True
        "json_schema_extra": {
            "example": {
                "quantity": 2,
                "status": "PENDING",
                "user_id": 1,
            }
        }
    }

class OrderStatusModel(BaseModel):
    status: Optional[str] = "PENDING"

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "status": "PENDING",
            }
        }
    }