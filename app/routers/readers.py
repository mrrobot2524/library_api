from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.post("/", response_model=schemas.ReaderOut)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.create_reader(db, reader)


@router.get("/", response_model=list[schemas.ReaderOut])
def read_readers(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_readers(db)


@router.get("/{reader_id}", response_model=schemas.ReaderOut)
def read_reader(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    reader = crud.get_reader(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@router.put("/{reader_id}", response_model=schemas.ReaderOut)
def update_reader(reader_id: int, reader: schemas.ReaderUpdate, db: Session = Depends(get_db),
                  user=Depends(get_current_user)):
    updated = crud.update_reader(db, reader_id, reader)
    if not updated:
        raise HTTPException(status_code=404, detail="Reader not found")
    return updated


@router.delete("/{reader_id}", response_model=schemas.ReaderOut)
def delete_reader(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    deleted = crud.delete_reader(db, reader_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reader not found")
    return deleted
