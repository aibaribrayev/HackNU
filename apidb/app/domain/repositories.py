from typing import List
from sqlalchemy.orm import Session
from .models import Product, Zakupki, Sales

class ProductRepository:
    def get_by_id(db: Session, product_id: int):
        return db.query(Product).filter(Product.product_id == product_id).first()

    # Add other methods for CRUD operations here.

class ZakupkiRepository:
    def get_by_price_id(db: Session, price_id: int):
        return db.query(Zakupki).filter(Zakupki.price_id == price_id).first()

    # Add other methods for CRUD operations
