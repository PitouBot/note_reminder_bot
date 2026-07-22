import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMINS = list(map(int, os.getenv("ADMINS", "").split(','))) if os.getenv("ADMINS") else []
