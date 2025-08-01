from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_number = Column(String, nullable=False)
    enable_2fa = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CoffeeShop(Base):
    __tablename__ = "coffee_shops"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float)
    status = Column(String)
    image = Column(String)
    
    # Relationship with Drink model
    drinks = relationship("Drink", back_populates="coffee_shop", cascade="all, delete-orphan")

class Drink(Base):
    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(String)
    image = Column(String)
    sales = Column(Integer, default=0)
    popularity = Column(Integer, default=0)
    
    # Foreign key to CoffeeShop
    coffee_shop_id = Column(Integer, ForeignKey("coffee_shops.id"))
    
    # Relationship with CoffeeShop model
    coffee_shop = relationship("CoffeeShop", back_populates="drinks")

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    thumbnail = Column(String, nullable=True)
    uploaded_at = Column(String)