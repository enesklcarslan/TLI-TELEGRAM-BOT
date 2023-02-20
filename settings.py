import os

from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.environ.get("BASE_URL")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")