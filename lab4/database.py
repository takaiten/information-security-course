from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder

# SQLALCHEMY_DATABASE_URL = 'postgresql://dba:gamermoment@217.71.129.139:4195/phone_book_db'
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )

server = SSHTunnelForwarder(
    ('ssh.cloud.nstu.ru', 5330),
    ssh_username='dba',
    ssh_password='gamermoment',
    remote_bind_address=('127.0.0.1', 5432)
    )

server.start()
local_port = str(server.local_bind_port)

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format('dba', 'gamermoment', '127.0.0.1', local_port, 'phone_book_db'))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
