from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder

from .configs.connection import *

server = SSHTunnelForwarder(
    (SSH_HOST, SSH_PORT),
    ssh_username=USERNAME,
    ssh_password=PASSWORD,
    remote_bind_address=(REMOTE_HOST, REMOTE_PORT)
)

server.start()
local_port = str(server.local_bind_port)

engine = create_engine(f'postgresql://{USERNAME}:{PASSWORD}@{REMOTE_HOST}:{local_port}/{DATABASE}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
