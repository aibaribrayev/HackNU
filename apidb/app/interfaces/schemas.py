from pydantic import BaseModel

class ProductSchema(BaseModel):
    user_id: int
    product_id: int
    price_id: int

    class Config:
        orm_mode = True
