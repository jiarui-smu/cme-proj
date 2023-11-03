from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USER = os.environ.get("MYSQL_USER")
DATABASE_PASSWORD = os.environ.get("MYSQL_PASSWORD")
PORT = str(os.environ.get("MYSQL_PORT"))
MAC_USER = USER+":"+DATABASE_PASSWORD
MAC_PORT = str(os.environ.get("MYSQL_MAC_PORT"))
SQLALCHEMY_DATABASE_URI = str(os.environ.get("SQLALCHEMY_DATABASE_URI"))

# gets env variables from .env file  for local machine testing