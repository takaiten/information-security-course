from sqlalchemy import Column, ForeignKey, Integer, String, Sequence
from sqlalchemy.orm import relationship

from .database import Base


class Role(Base):
    __tablename__ = 'roles'

    roles_id_seq = Sequence('roles_id_seq')

    id = Column(Integer, roles_id_seq, primary_key=True, server_default=roles_id_seq.next_value())
    name = Column(String)

    users = relationship('User', back_populates='owner')


class User(Base):
    __tablename__ = 'users'

    users_id_seq = Sequence('users_id_seq')

    id = Column(Integer, users_id_seq, primary_key=True, server_default=users_id_seq.next_value())
    name = Column(String)   # Text
    email = Column(String, unique=True)  # Text
    salt = Column(String)   # Column(Char())
    hash = Column(String)   # CHAR(length=10)
    role_id = Column(Integer, ForeignKey('roles.id'))

    owner = relationship('Role', back_populates='users')


class Phonebook(Base):
    __tablename__ = 'phonebook'

    phonebook_id_seq = Sequence('phonebook_id_seq')

    id = Column(Integer, phonebook_id_seq, primary_key=True, server_default=phonebook_id_seq.next_value())
    name = Column(String)   # Text
    telephone = Column(String, unique=True)  # VARCHAR(length=15)
    address = Column(String)    # Text


class SerialNumber(Base):
    __tablename__ = 'serial_numbers'

    serial_number = Column(String, primary_key=True)    # CHAR(length=16)
