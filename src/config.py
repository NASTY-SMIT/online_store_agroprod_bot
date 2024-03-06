import logging
import os

from dotenv import load_dotenv
import telebot
import sqlite3 as sl

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

con = sl.connect("database.db", check_same_thread=False)

token = os.getenv("TOKEN")

if token is None:
    raise ValueError("Токен не найден в файле .env")

bot = telebot.TeleBot(token)
