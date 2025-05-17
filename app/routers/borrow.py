from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/borrow", tags=["Borrowing"])


@router.post("/issue", response_model=schemas.BorrowedBookOut)
def borrow_book(data: schemas.BorrowRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return crud.borrow_book(db, data.book_id, data.reader_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/return", response_model=schemas.BorrowedBookOut)
def return_book(data: schemas.ReturnRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return crud.return_book(db, data.borrow_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reader/{reader_id}", response_model=list[schemas.BorrowedBookOut])
def reader_active_borrows(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_reader_active_books(db, reader_id)
