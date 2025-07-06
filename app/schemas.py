from pydantic import BaseModel, Field
from datetime import datetime

class KraftwertBase(BaseModel):
    muskelgruppe: str = Field(..., example="Brust")
    uebung: str = Field(..., example="Bankdrücken")
    gewicht: float = Field(..., example=80.5)

class KraftwertCreate(KraftwertBase):
    pass

class KraftwertUpdate(KraftwertBase):
    pass

class Kraftwert(KraftwertBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True