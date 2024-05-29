import os
import gettext
from aiogram import Router, F
from aiogram.types import Message, PhotoSize, ContentType
from aiogram.filters import Command
from imageprocessor import ImageProcessor
from translator import TranslatorService

# Locale files loading
translations = {
    "en": gettext.translation('messages', localedir='locale', languages=['en']),
    "ru": gettext.translation('messages', localedir='locale', languages=['ru']),
}
# Using english language for default
current_translation = translations["en"]
_ = current_translation.gettext  # Define _ as locale function
user_languages = {}

router = Router()


def set_language(user_id, lang_code):
    user_languages[user_id] = lang_code
    global current_translation, _
    current_translation = translations[lang_code]
    _ = current_translation.gettext  # Define _ as locale function
    current_translation.install()


@router.message(Command("start"))
async def start_handler(msg: Message):
    """Start message handler"""
    await msg.answer(_("start_message"))


@router.message(Command("language"))
async def language_handler(msg: Message):
    await msg.answer(_("language_prompt"))


@router.message(Command("en"))
async def set_language_en(msg: Message):
    set_language(msg.from_user.id, "en")
    await msg.answer(_("language_set"))


@router.message(Command("ru"))
async def set_language_ru(msg: Message):
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
        translator = TranslatorService(to_lang=user_lang)

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
    """Message handler"""
    await msg.answer("Send me an image and I try to predict what is it.")


@router.message()
async def unknown_message_handler(msg: Message):
    """Unknown command handler"""
    await msg.answer(_("unknown_command").format(user_id=msg.from_user.id))
