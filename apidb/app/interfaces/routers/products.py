from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.domain.repositories import ProductRepository
from app.domain.models import Product
from app.interfaces.schemas import ProductSchema
from app.infrastructure.db import get_db

router = APIRouter()


@router.get("/products/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductRepository.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
