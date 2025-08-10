import os
from dotenv import load_dotenv

# .env fayldan ma'lumotlarni yuklaymiz
load_dotenv()

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# O'yin sozlamalari
MIN_PLAYERS = 2   # Eng kam o'yinchi soni
MAX_PLAYERS = 10  # Eng ko'p o'yinchi soni

# Tillar
LANGUAGES = ["uz", "en"]

# Fayl nomlari
DATA_FILE = "data.json"
LOCALES_DIR = "locales/"

