from sqlalchemy.orm import Session
from . import models, auth, schemas
from datetime import datetime


def create_user(db: Session, email: str, password: str):
    hashed = auth.hash_password(password)
    user = models.User(email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# BOOK CRUD
def create_book(db: Session, book_data: schemas.BookCreate):
    book = models.Book(**book_data.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session):
    return db.query(models.Book).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, data: schemas.BookUpdate):
    book = get_book(db, book_id)
    if not book:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        return None
    db.delete(book)
    db.commit()
    return book


# READER CRUD
def create_reader(db: Session, data: schemas.ReaderCreate):
    reader = models.Reader(**data.dict())
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


def get_readers(db: Session):
    return db.query(models.Reader).all()


def get_reader(db: Session, reader_id: int):
    return db.query(models.Reader).filter(models.Reader.id == reader_id).first()


def update_reader(db: Session, reader_id: int, data: schemas.ReaderUpdate):
    reader = get_reader(db, reader_id)
    if not reader:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(reader, key, value)
    db.commit()
    db.refresh(reader)
    return reader


def delete_reader(db: Session, reader_id: int):
    reader = get_reader(db, reader_id)
    if not reader:
        return None
    db.delete(reader)
    db.commit()
    return reader


# Получить активные книги у читателя
def get_active_borrow_count(db: Session, reader_id: int):
    return db.query(models.BorrowedBook).filter(
        models.BorrowedBook.reader_id == reader_id,
        models.BorrowedBook.return_date == None
    ).count()


def borrow_book(db: Session, book_id: int, reader_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book or book.quantity <= 0:
        raise ValueError("Книга не найдена или закончились экземпляры")

    active_borrows = get_active_borrow_count(db, reader_id)
    if active_borrows >= 3:
        raise ValueError("Читатель уже взял максимум 3 книги")

    # Всё ок — выдаём
    book.quantity -= 1
    borrow = models.BorrowedBook(book_id=book_id, reader_id=reader_id)
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


def return_book(db: Session, borrow_id: int):
    borrow = db.query(models.BorrowedBook).filter(models.BorrowedBook.id == borrow_id).first()
    if not borrow or borrow.return_date is not None:
        raise ValueError("Книга не найдена или уже возвращена")

    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    book.quantity += 1
    borrow.return_date = datetime.utcnow()
    db.commit()
    db.refresh(borrow)
    return borrow


def get_reader_active_books(db: Session, reader_id: int):
    return db.query(models.BorrowedBook).filter(
        models.BorrowedBook.reader_id == reader_id,
        models.BorrowedBook.return_date == None
    ).all()
