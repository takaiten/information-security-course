from sqlalchemy import Column, ForeignKey, Integer, String, Sequence

from .database import Base


class Role(Base):
    __tablename__ = 'roles'

    roles_id_seq = Sequence('roles_id_seq')

    id = Column(Integer, roles_id_seq, primary_key=True, server_default=roles_id_seq.next_value())
    name = Column(String, unique=True, nullable=False)


class User(Base):
    __tablename__ = 'users'

    users_id_seq = Sequence('users_id_seq')

    id = Column(Integer, users_id_seq, primary_key=True, server_default=users_id_seq.next_value())
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    salt = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))


class Phonebook(Base):
    __tablename__ = 'phonebook'

    phonebook_id_seq = Sequence('phonebook_id_seq')

    id = Column(Integer, phonebook_id_seq, primary_key=True, server_default=phonebook_id_seq.next_value())
    name = Column(String, nullable=False)
    telephone = Column(String, unique=True, nullable=False)
    address = Column(String)


class SerialNumber(Base):
    __tablename__ = 'serial_numbers'

    serial_number = Column(String, primary_key=True)
