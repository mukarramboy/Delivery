from pydantic import BaseModel
from typing import Optional



class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

    
    model_config = {
        "from_attributes": True,  # заменяет orm_mode = True
        "json_schema_extra": {
            "example": {
                "name": "Sample Product",
                "description": "This is a sample product description.",
                "price": 19.99,
                "in_stock": True
            }
        }
    }