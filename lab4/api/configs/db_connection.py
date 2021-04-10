import os
from dotenv import load_dotenv

load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = os.getenv('SSH_PORT')

REMOTE_HOST = os.getenv('REMOTE_HOST')
REMOTE_PORT = os.getenv('REMOTE_PORT')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

DATABASE = os.getenv('DATABASE')
