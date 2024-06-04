from aiogram import Router, F
from aiogram.types import Message, PhotoSize, ContentType, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from imageprocessor import ImageProcessor
from translator import TranslatorService
from database import Database
import os

router = Router()
global _

# Define language commands keyboard
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/en"), KeyboardButton(text="/ru")]
    ],
    resize_keyboard=True
)

# Define main commands keyboard
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Info")],
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/language")]
    ],
    resize_keyboard=True
)


@router.message(Command('start'))
async def start_handler(msg: Message):
    """Start message handler"""
    db = Database()
    user_locale = db.get_user_locale(msg.from_user.id)

    if user_locale is None:
        db.add_user(msg.from_user.id, 'en')

    await msg.answer(_('start_message'), reply_markup=main_keyboard)


@router.message(Command('language'))
async def language_handler(msg: Message):
    """Language message handler"""
    await msg.answer(_('language_prompt'), reply_markup=language_keyboard)


@router.message(Command('en'))
async def set_language_en(msg: Message):
    """En message handler"""
    db = Database()
    db.update_user_locale(msg.from_user.id, 'en')
    await msg.answer(_('language_set'), reply_markup=main_keyboard)


@router.message(Command('ru'))
async def set_language_ru(msg: Message):
    """Ru message handler"""
    db = Database()
    db.update_user_locale(msg.from_user.id, 'ru')
    await msg.answer(_('language_set'), reply_markup=main_keyboard)


@router.message(F.content_type == ContentType.PHOTO)
async def image_handler(msg: Message):
    """Image handler"""
    image: PhotoSize = msg.photo[-1]  # Largest image
    await msg.answer(_('image_processing'))
    image_path = f'{image.file_id}.jpg'
    await msg.bot.download(file=image.file_id, destination=image_path)  # Downloading an image

    try:
        predictions = ImageProcessor.predict_image(image_path)  # Making prediction

        db = Database()
        user_lang = db.get_user_locale(msg.from_user.id)

        translator = TranslatorService(dest=user_lang)

        response = _('image_response')
        for i, (imagenet_id, label, score) in enumerate(predictions):
            translated_label = translator.translate_text(label.replace('_', ' '))
            translated_text = translator.translate_text('with probability')
            response += f'{i + 1}. {translated_label} {translated_text} {score * 100:.2f}%\n'

        await msg.answer(response)
    finally:
        os.remove(image_path)  # Deleting local file


@router.message(F.content_type == ContentType.TEXT)
async def text_message_handler(msg: Message):
    """Text message handler"""
    await msg.answer(_('text_message'), reply_markup=main_keyboard)


@router.message()
async def unknown_message_handler(msg: Message):
    """Unknown message handler"""
    await msg.answer(_('unknown_command'), reply_markup=main_keyboard)
