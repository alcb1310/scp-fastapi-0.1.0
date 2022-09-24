from sqlalchemy import Column, String
from src.database import Base

class Test(Base):
    __tablename__ = "test"
    
    uuid = Column(String, primary_key=True)
    name = Column(String)
    
    class Config:
        orm_mode = True