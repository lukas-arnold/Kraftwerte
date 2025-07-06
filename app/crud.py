from sqlalchemy.orm import Session

from app.models import KraftwertDB
from app.schemas import KraftwertCreate, KraftwertUpdate

def get_kraftwert(db: Session, kraftwert_id: int):
    return db.query(KraftwertDB).filter(KraftwertDB.id == kraftwert_id).first()

def get_kraftwerte(db: Session, skip: int = 0, limit: int = 100):
    return db.query(KraftwertDB).order_by(KraftwertDB.muskelgruppe, KraftwertDB.uebung).offset(skip).limit(limit).all()

def create_kraftwert(db: Session, kraftwert: KraftwertCreate):
    db_kraftwert = KraftwertDB(**kraftwert.model_dump())
    db.add(db_kraftwert)
    db.commit()
    db.refresh(db_kraftwert)
    return db_kraftwert

def update_kraftwert(db: Session, kraftwert_id: int, kraftwert: KraftwertUpdate):
    db_kraftwert = db.query(KraftwertDB).filter(KraftwertDB.id == kraftwert_id).first()
    if db_kraftwert:
        for key, value in kraftwert.model_dump().items():
            setattr(db_kraftwert, key, value)
        db.commit()
        db.refresh(db_kraftwert)
    return db_kraftwert

def delete_kraftwert(db: Session, kraftwert_id: int):
    db_kraftwert = db.query(KraftwertDB).filter(KraftwertDB.id == kraftwert_id).first()
    if db_kraftwert:
        db.delete(db_kraftwert)
        db.commit()
        return True
    return False