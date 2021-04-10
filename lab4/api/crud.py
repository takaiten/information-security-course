from sqlalchemy.orm import Session

from . import models, schemas

from .utils.crypto import hash_password, generate_salt
from .configs.defaults import *


# --- COMMON --- #


def get_by_primary_key(db: Session, primary_key, model):
    return db.get(model, primary_key)


def get_by_value(db: Session, value, model, model_value):
    return db.query(model).filter(model_value == value).first()


def get_all(db: Session, model, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT):
    return db.query(model).offset(offset).limit(limit).all()


# --- ROLES --- #

def get_roles(db: Session, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT):
    return db.query(models.Role).offset(offset).limit(limit).all()


# --- USERS --- #

def get_user(db: Session, user_id: int):
    return get_by_primary_key(db, primary_key=user_id, model=models.User)


def get_user_by_email(db: Session, email: str):
    return get_by_value(db, value=email, model=models.User, model_value=models.User.email)


def get_users(db: Session, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT):
    return get_all(db, model=models.User, offset=offset, limit=limit)


def get_user_role_id(db: Session, user_id: int):
    db_user = get_user(db, user_id=user_id)

    if db_user is None:
        return None

    return db_user.role_id


def create_user(db: Session, user: schemas.UserCreate):
    salt = generate_salt()
    hashed_password = hash_password(password=user.password, salt=salt)

    user_data = user.dict()
    user_data.pop('password')

    db_user = models.User(**user_data, salt=salt, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    deleted_count = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()

    return deleted_count


# --- PHONEBOOK --- #

def get_phonebook_entry(db: Session, phone_id: int):
    return get_by_primary_key(db, primary_key=phone_id, model=models.Phonebook)


def get_phonebook_entry_by_telephone(db: Session, telephone: str):
    return get_by_value(db, value=telephone, model=models.Phonebook, model_value=models.Phonebook.telephone)


def get_phonebook(db: Session, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT):
    return get_all(db, model=models.Phonebook, offset=offset, limit=limit)


def create_phonebook_entry(db: Session, phone: schemas.PhoneCreate):
    db_phone = models.Phonebook(**phone.dict())

    db.add(db_phone)
    db.commit()
    db.refresh(db_phone)

    return db_phone


def delete_phonebook_entry(db: Session, phone_id: int):
    deleted_count = db.query(models.Phonebook).filter(models.Phonebook.id == phone_id).delete()
    db.commit()

    return deleted_count


# --- SERIAL NUMBERS --- #

def get_serial_number(db: Session, serial_number: str):
    return db.get(models.SerialNumber, serial_number)
