from aiogram import Router, F
from aiogram.types import Message, PhotoSize, ContentType
from aiogram.filters import Command
from imageprocessor import ImageProcessor
from translator import TranslatorService
from database import Database
import os
import gettext

# Locale files loading
translations = {
    "en": gettext.translation('messages', localedir='locale', languages=['en']),
    "ru": gettext.translation('messages', localedir='locale', languages=['ru']),
}
current_translation = translations["en"]  # Using english language for default
_ = current_translation.gettext  # Define _ as locale function
user_languages = {}

router = Router()


def set_language(user_id, lang_code):
    """Language setting function"""
    user_languages[user_id] = lang_code
    global current_translation, _
    current_translation = translations[lang_code]
    _ = current_translation.gettext  # Define _ as locale function
    current_translation.install()


@router.message(Command('start'))
async def start_handler(msg: Message):
    """Start message handler"""
    db = Database()
    if msg.from_user.id not in db.custom_query('SELECT Users.id FROM Users'):
        db.add_user(msg.from_user.id, 'en')

    await msg.answer(_("start_message"))


@router.message(Command('language'))
async def language_handler(msg: Message):
    """Language message handler"""
    await msg.answer(_('language_prompt'))


@router.message(Command("en"))
async def set_language_en(msg: Message):
    """En message handler"""
    db = Database()
    db.update_user(msg.from_user.id, "en")
    set_language(msg.from_user.id, "en")
    await msg.answer(_("language_set"))


@router.message(Command("ru"))
async def set_language_ru(msg: Message):
    """Ru message handler"""
    db = Database()
    db.update_user(msg.from_user.id, "ru")
    set_language(msg.from_user.id, "ru")
    await msg.answer(_("language_set"))


@router.message(F.content_type == ContentType.PHOTO)
async def image_handler(msg: Message):
    """Image handler"""
    image: PhotoSize = msg.photo[-1]  # Largest image

    await msg.answer(_("image_processing"))

    image_path = f"{image.file_id}.jpg"
    await msg.bot.download(file=image.file_id, destination=image_path)  # Downloading an image

    try:
        predictions = ImageProcessor.predict_image(image_path)  # Making prediction

        user_lang = user_languages.get(msg.from_user.id, "en")
        translator = TranslatorService(dest=user_lang)

        response = _("image_response")
        for i, (imagenet_id, label, score) in enumerate(predictions):
            translated_label = translator.translate_text(label.replace('_', ' '))
            translated_text = translator.translate_text("with probability")
            response += f"{i + 1}. {translated_label} {translated_text} {score * 100:.2f}%\n"

        await msg.answer(response)
    finally:
        os.remove(image_path)  # Deleting local file


@router.message(F.content_type == ContentType.TEXT)
async def text_message_handler(msg: Message):
    """Text message handler"""
    await msg.answer(_("text_message"))


@router.message()
async def unknown_message_handler(msg: Message):
    """Unknown message handler"""
    await msg.answer(_("unknown_command"))
