from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class KraftwertDB(Base):
    __tablename__ = "strength_data"

    id = Column(Integer, primary_key=True, index=True)
    muskelgruppe = Column(String, nullable=False)
    uebung = Column(String, nullable=False)
    gewicht = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())