from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models.db_config import Base
import enum

class CurrencyEnum(enum.Enum):
    USD = "$"
    EUR = "€"
    MAD = "DH"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    currency = Column(Enum(CurrencyEnum), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    budget_entries = relationship("Budget", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), unique=True, nullable=False)
    category_description = Column(String)
    
    budget_entries = relationship("Budget", back_populates="category")

class Budget(Base):
    __tablename__ = "budget"

    entry_id = Column(Integer, primary_key=True, autoincrement=True)
    usr_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    entry_date = Column(Date, nullable=False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    amount = Column(Float, nullable=False)

    user = relationship("User", back_populates="budget_entries")
    category = relationship("Category", back_populates="budget_entries")