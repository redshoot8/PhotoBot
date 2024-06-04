from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update
from database import Database
import gettext

# Locale files loading
translations = {
    'en': gettext.translation('messages', localedir='locale', languages=['en']),
    'ru': gettext.translation('messages', localedir='locale', languages=['ru']),
}


class LanguageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
        else:
            return await handler(event, data)

        db = Database()
        user_locale = db.get_user_locale(user_id)

        if user_locale:
            current_translation = translations[user_locale]
        else:
            current_translation = translations['en']

        global _
        _ = current_translation.gettext
        current_translation.install()

        return await handler(event, data)
