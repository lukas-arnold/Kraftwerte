from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/kraftwerte",
    tags=["Kraftwerte"]
)

@router.post("/", response_model=schemas.Kraftwert, status_code=201)
def create_kraftwert_route(kraftwert: schemas.KraftwertCreate, db: Session = Depends(get_db)):
    return crud.create_kraftwert(db=db, kraftwert=kraftwert)

@router.get("/", response_model=List[schemas.Kraftwert])
def read_kraftwerte_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    kraftwerte = crud.get_kraftwerte(db, skip=skip, limit=limit)
    return kraftwerte

@router.get("/{kraftwert_id}", response_model=schemas.Kraftwert)
def read_kraftwert_route(kraftwert_id: int, db: Session = Depends(get_db)):
    db_kraftwert = crud.get_kraftwert(db, kraftwert_id=kraftwert_id)
    if db_kraftwert is None:
        raise HTTPException(status_code=404, detail="Kraftwert nicht gefunden")
    return db_kraftwert

@router.put("/{kraftwert_id}", response_model=schemas.Kraftwert)
def update_kraftwert_route(kraftwert_id: int, kraftwert: schemas.KraftwertUpdate, db: Session = Depends(get_db)):
    db_kraftwert = crud.update_kraftwert(db, kraftwert_id=kraftwert_id, kraftwert=kraftwert)
    if db_kraftwert is None:
        raise HTTPException(status_code=404, detail="Kraftwert nicht gefunden")
    return db_kraftwert

@router.delete("/{kraftwert_id}", status_code=204)
def delete_kraftwert_route(kraftwert_id: int, db: Session = Depends(get_db)):
    success = crud.delete_kraftwert(db, kraftwert_id=kraftwert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Kraftwert nicht gefunden")
    return {"message": "Kraftwert erfolgreich gelöscht"}