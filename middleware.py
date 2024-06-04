from aiogram import BaseMiddleware
from aiogram.types import Update
from database import Database
import gettext

# Locale files loading
translations = {
    'en': gettext.translation('messages', localedir='locale', languages=['en']),
    'ru': gettext.translation('messages', localedir='locale', languages=['ru']),
}


class LanguageMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_update(self, update: Update):
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        else:
            return

        db = Database()
        user_locale = db.get_user_locale(user_id)

        if user_locale:
            current_translation = translations[user_locale]
        else:
            current_translation = translations['en']

        global _
        _ = current_translation.gettext
        current_translation.install()
