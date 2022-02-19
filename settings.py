import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

# base settings
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
