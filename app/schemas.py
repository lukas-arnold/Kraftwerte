from pydantic import BaseModel
from datetime import datetime

class KraftwertBase(BaseModel):
    muskelgruppe: str
    uebung: str
    gewicht: float

class KraftwertCreate(KraftwertBase):
    pass

class KraftwertUpdate(KraftwertBase):
    pass

class Kraftwert(KraftwertBase):
    id: int
    updated_at: datetime

    class ConfigDict:
        from_attributes = True