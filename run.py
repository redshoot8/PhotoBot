import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


async def run():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        raise FileNotFoundError
    bot = Bot(token=os.getenv('BOT_TOKEN'))