from sqlalchemy.orm import Session

from . import models, schemas

from .constants.defaults import *


# --- ROLES --- #

def get_roles(db: Session, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT):
    return db.query(models.Role).offset(offset).limit(limit).all()


# --- USERS --- #

def get_user(db: Session, user_id: int):
    return db.get(models.User, user_id)
    # return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT):
    return db.query(models.User).offset(offset).limit(limit).all()


def get_user_role_id(db: Session, user_id: int):
    db_user = get_user(db, user_id=user_id)

    if db_user is None:
        return None

    return db_user.role_id


def create_user(db: Session, user: schemas.UserCreate):
    salt = 'salt'
    hashed_password = salt + user.password  # TODO: use hash

    db_user = models.User(**user.dict().pop('password'), salt=salt, hash=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user_data(db: Session, user_id: int, user_data: schemas.UserUpdate):
    updated_count = db.query(models).filter(models.User.id == user_id).update(**user_data.dict())
    db.commit()

    return updated_count


def delete_user(db: Session, user_id: int):
    deleted_count = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()

    return deleted_count


# --- Phonebook --- #

def get_phone(db: Session, phone_id: int):
    return db.get(models.Phonebook, phone_id)


def get_phone_by_number(db: Session, phone_number: str):
    return db.query(models.Phonebook).filter(models.Phonebook.telephone == phone_number).first()


def get_phonebook(db: Session, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT):
    phonebook = db.query(models.Phonebook).offset(offset).limit(limit).all()

    return phonebook


def create_phone_number(db: Session, role_id: int, phone: schemas.PhoneCreate):
    db_phone = models.Phonebook(**phone.dict())

    db.add(db_phone)
    db.commit()
    db.refresh(db_phone)

    return db_phone


def delete_phone(db: Session, phone_id: int):
    deleted_count = db.query(models.Phonebook).filter(models.Phonebook.id == phone_id).delete()
    db.commit()

    return deleted_count


# --- SERIAL NUMBERS --- #

def get_serial_number(db: Session, serial_number: str):
    return db.get(models.SerialNumber, serial_number)
