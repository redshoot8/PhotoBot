from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router
from background import keep_alive
import asyncio
import logging
import os


def prepare_environment():
    """Environment preparing function"""
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        raise FileNotFoundError(".env file not found.")


async def main():
    """Main function"""
    logging.basicConfig(filename="bot_log.log",
                        filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    prepare_environment()

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
