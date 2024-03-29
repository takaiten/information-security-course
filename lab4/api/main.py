from typing import List, Dict

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from . import crud, models, schemas
from .database import SessionLocal, engine

from .utils.crypto import hash_sha256

from .configs.defaults import *
from .configs.roles import *
from .configs.app_config import *


# --- APP --- #

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)

deny_set = set()


# --- METHODS --- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorize: AuthJWT):
    authorize.jwt_required()
    return authorize.get_jwt_subject()


@AuthJWT.load_config
def get_config():
    return schemas.Settings()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in deny_set


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
    )


# --- LOGIN --- #

@app.post('/login', response_model=schemas.UserWithToken)
def login(user_login_data: schemas.UserLogin, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_refresh_token_required()

    user = crud.get_user_by_email(db, user_login_data.email)

    if user is None:
        raise HTTPException(status_code=401, detail='Invalid email')

    if hash_sha256(user_login_data.password + user.salt) != user.hashed_password:
        raise HTTPException(status_code=401, detail='Invalid password')

    access_token = authorize.create_access_token(subject=user.id)

    return {'access_token': access_token, 'user': user}


@app.post('/logout', response_model=Dict[str, str])
def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    jti = authorize.get_raw_jwt()['jti']
    deny_set.add(jti)
    return {'detail': 'Access token has been revoke'}


# --- SERIAL NUMBER --- #

@app.get('/serial_number/', response_model=str)
def check_serial_number(serial_number: str, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_serial_number = crud.get_serial_number(db, serial_number=serial_number.lower())

    if db_serial_number is None:
        raise HTTPException(status_code=400, detail='Invalid serial number')

    return authorize.create_refresh_token(subject=db_serial_number.serial_number)


# --- ROLES --- #

@app.get('/roles/', response_model=List[schemas.Role])
def get_roles(offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT,
              authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()

    return crud.get_roles(db, offset=offset, limit=limit)


# --- USERS --- #

@app.get('/users/me', response_model=schemas.User)
def get_user_current(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    current_user_id = get_current_user(authorize)

    db_user = crud.get_user(db, user_id=current_user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return db_user

@app.get('/users/{user_id}', response_model=schemas.User)
def get_user(user_id: int, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()

    db_user = crud.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return db_user


@app.get('/users/', response_model=List[schemas.User])
def get_users(offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT,
              authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()

    return crud.get_users(db, offset=offset, limit=limit)


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    current_user = get_current_user(authorize)

    if crud.get_user_role_id(db, user_id=current_user) != ADMIN_ID:
        raise HTTPException(status_code=403, detail='Not enough authority')

    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail='Email already registered')

    try:
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='No role with such id')


@app.delete('/users/{user_id}')
def delete_user(user_id: int, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    current_user = get_current_user(authorize)

    if crud.get_user_role_id(db, user_id=current_user) != ADMIN_ID:
        raise HTTPException(status_code=403, detail='Not enough authority')

    if crud.delete_user(db, user_id=user_id) == 0:
        raise HTTPException(status_code=400, detail='No user with such id')


# --- PHONEBOOK --- #

@app.get('/phonebook/', response_model=List[schemas.Phone])
def get_phonebook(offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT,
                  authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()

    return crud.get_phonebook(db, offset=offset, limit=limit)


@app.post('/phonebook/', response_model=schemas.Phone)
def create_phonebook_entry(phone: schemas.PhoneCreate, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    current_user = get_current_user(authorize)

    if crud.get_user_role_id(db, user_id=current_user) == USER_ID:
        raise HTTPException(status_code=403, detail='Not enough authority')

    if crud.get_phonebook_entry_by_telephone(db, telephone=phone.telephone):
        raise HTTPException(status_code=400, detail='Phone already registered')

    return crud.create_phonebook_entry(db, phone=phone)


@app.delete('/phonebook/{phone_id}')
def delete_phone(phone_id: int, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    current_user = get_current_user(authorize)

    if crud.get_user_role_id(db, user_id=current_user) == USER_ID:
        raise HTTPException(status_code=403, detail='Not enough authority')

    if crud.get_phonebook_entry(db, phone_id=phone_id) is None:
        raise HTTPException(status_code=404, detail='No such phone')

    if crud.delete_phonebook_entry(db, phone_id=phone_id) == 0:
        raise HTTPException(status_code=400, detail='No phone with such id')
