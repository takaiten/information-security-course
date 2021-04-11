from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values()

connection_string = ('postgresql://' +
                     config['USERNAME'] + ':' + config['PASSWORD'] + '@' +
                     config['REMOTE_HOST'] + ':' + config['REMOTE_PORT'] + '/' +
                     config['DATABASE'])

engine = create_engine(connection_string)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
