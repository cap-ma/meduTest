from django.core.management.base import BaseCommand
from dotenv import load_dotenv
import os
from django.conf import settings
from asgiref.sync import sync_to_async

"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types
from education.models import Test
from user.models import User, StudentProfile, TeacherProfile

API_TOKEN = settings.BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    student = await StudentProfile.objects.aget(
        parent_teleg_account=str(message.from_user.username)
    )

    if student:
        user = await User.objects.aget(student_profile=student)
        student.verification_for_bot = True
        student.parent_telegram_id = str(message.from_user.id)
        await student.asave()

        await message.answer(
            f"Sizning ma'lumotlaringiz {user.first_name} {user.last_name}\n Siz Ma'lumotlarni tasdiqlaysizmi"
        )
    else:
        await message.answer("Sizning ma'lumotlaringiz topilmadi")


@dp.message_handler(regexp="(^cat[s]?$|puss)")
async def cats(message: types.Message):
    with open("data/cats.jpg", "rb") as photo:
        """
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        """

        await message.reply_photo(photo, caption="Cats are here 😺")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=True)
