from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router
from background import keep_alive
from middleware import LanguageMiddleware
import asyncio
import logging
import os


def prepare_environment():
    """Environment preparing function"""
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        raise FileNotFoundError('.env file not found.')


async def main():
    """Main function"""
    logging.basicConfig(filename='bot_log.log',
                        filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    prepare_environment()

    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(LanguageMiddleware())
    dp.include_router(router)

    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/language", description="Set language"),
        BotCommand(command="/en", description="Set language to English"),
        BotCommand(command="/ru", description="Set language to Russian"),
    ]
    await bot.set_my_commands(commands)

    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
