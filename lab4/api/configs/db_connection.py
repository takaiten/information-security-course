import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(BASEDIR + '/db_config.env', verbose=True)

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT'))

REMOTE_HOST = os.getenv('REMOTE_HOST')
REMOTE_PORT = int(os.getenv('REMOTE_PORT'))

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

DATABASE = os.getenv('DATABASE')
