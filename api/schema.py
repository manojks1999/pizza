import re
import ast
import string

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, Boolean, TIMESTAMP, Sequence, Date, VARCHAR, BIGINT


from api import Base

from datetime import datetime, timedelta, timezone
import uuid

# env
# from dotenv import load_dotenv
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    DateTime,
    BigInteger,
    Float,
    JSON,
    ForeignKey,
    TIMESTAMP,
)
import os

# env
# from dotenv import load_dotenv

# load environment variables
# load_dotenv()
# get environment
ENVIRONMENT = os.environ.get("ENVIRONMENT")


# python classes that connect with the central
# db and provide classes to connect with tables
class Items(Base):
    __tablename__ = "items"
    __table_args__ = {"extend_existing": True}
    name = Column(VARCHAR)
    price = Column(Integer)
    category = Column(VARCHAR, nullable=False)
    id = Column(VARCHAR, primary_key=True)

    def __init__(
        self,
        name,
        price,
        category
    ):
        """
        Create object
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.category = category

    def to_dict(self):
        item_data = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
        }
        return item_data
    
class Orders(Base):
    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}
    quantity = Column(Integer)
    total_price = Column(Float)
    item = Column(JSON)
    status = Column(VARCHAR)
    ordered_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    id = Column(VARCHAR, primary_key=True)

    def __init__(
        self,
        quantity,
        total_price,
        item
    ):
        """
        Create object
        """
        self.id = str(uuid.uuid4())
        self.quantity = quantity
        self.total_price = total_price
        self.item = item
        self.ordered_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.updated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.status = 'placed'

    def to_dict(self):
        order_data = {
            "id": self.id,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "item": self.item,
            "ordered_at": self.ordered_at,
            "updated_at": self.updated_at,
            "status": self.status
        }
        return order_data