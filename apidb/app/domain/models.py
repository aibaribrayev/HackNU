from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    user_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    price_id = Column(Integer, ForeignKey('zakupki.price_id'), nullable=True)
    zakupki = relationship("Zakupki", back_populates="product")
    sales = relationship("Sales", back_populates="product")

class Zakupki(Base):
    __tablename__ = 'zakupki'
    user_id = Column(Integer, primary_key=True)
    price_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    datetime = Column(DateTime)
    sold_amount = Column(Float)
    bought_amount = Column(Float)
    product = relationship("Product", back_populates="zakupki")

class Sales(Base):
    __tablename__ = 'sales'
    user_id = Column(Integer, primary_key=True)
    price_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    datetime = Column(DateTime)
    amount_not_connected = Column(Float)
    product = relationship("Product", back_populates="sales")
