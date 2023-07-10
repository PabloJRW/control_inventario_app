from database import Base
from sqlalchemy import Column, Integer, String


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer)
    date = Column(String)
    time = Column(String)
