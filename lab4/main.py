from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .constants.defaults import *
from .constants.roles import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ROLES --- #

@app.get('/roles/', response_model=List[schemas.Role])
def get_roles(offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    roles = crud.get_roles(db, offset=offset, limit=limit)
    return roles


# --- USERS --- #

@app.get('/users/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return db_user


@app.get('/users/', response_model=List[schemas.User])
def get_users(offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT, db: Session = Depends(get_db)):
    users = crud.get_users(db, offset=offset, limit=limit)
    return users


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    return crud.create_user(db=db, user=user)


@app.patch('/users/{user_id}', response_model=int)
def update_user_data(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_count = crud.update_user_data(db, user_id=user_id, user_data=user_data)
    return updated_count


@app.delete('/users/{user_id}', response_model=int)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_count = crud.delete_user(db, user_id=user_id)
    return deleted_count


# TODO: authorization method


# --- Phonebook --- #

@app.get('/phonebook/', response_model=List[schemas.Phone])
def get_phonebook(user_id: int, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT,
                  db: Session = Depends(get_db)):
    db_user_role_id = crud.get_user_role_id(db, user_id=user_id)

    if db_user_role_id is None:
        raise HTTPException(status_code=404, detail='User not found')

    phonebook = crud.get_phonebook(db, offset=offset, limit=limit)

    if db_user_role_id == USER['id']:
        return list(map(lambda x: x.pop('address'), phonebook))

    return phonebook


@app.put('/phonebook/', response_model=int)
def add_phone(user_id: int, phone: schemas.PhoneCreate, db: Session = Depends(get_db)):
    db_user_role_id = crud.get_user_role_id(db, user_id=user_id)

    if db_user_role_id is None:
        raise HTTPException(status_code=404, detail='User not found')

    if db_user_role_id == USER['id']:
        raise HTTPException(status_code=403, detail='Not enough authority')

    db_phone = crud.get_phone_by_number(db, phone_number=phone.telephone)

    if db_phone:
        raise HTTPException(status_code=400, detail='Phone already registered')

    return crud.create_phone_number(db, phone=phone)


@app.delete('/phonebook/{phone_id}', response_model=int)
def delete_phone(user_id: int, phone_id: int, db: Session = Depends(get_db)):
    db_user_role_id = crud.get_user_role_id(db, user_id=user_id)

    if db_user_role_id is None:
        raise HTTPException(status_code=404, detail='User not found')

    if db_user_role_id == USER['id']:
        raise HTTPException(status_code=403, detail='Not enough authority')

    db_phone = crud.get_phone(db, phone_id=phone_id)

    if db_phone is None:
        raise HTTPException(status_code=404, detail='No such phone')

    return crud.delete_phone(db, phone_id=phone_id)


# --- SERIAL NUMBER --- #

@app.post('/serial_number/', response_model=str)
def check_serial_number(serial_number: str, db: Session = Depends(get_db)):
    # TODO: update serial number storage system

    db_serial_number = crud.get_serial_number(db, serial_number=serial_number)

    if db_serial_number is None:
        raise HTTPException(status_code=400, detail='Invalid serial number')

    return db_serial_number
