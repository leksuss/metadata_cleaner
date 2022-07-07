import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile

logging.basicConfig(level=logging.INFO)

load_dotenv()

dp = Dispatcher()
bot = Bot(os.getenv('TOKEN'), parse_mode="HTML")

@dp.message()
async def scan_message(message: types.Message):

    try:
        file_obj = message.document
    except Exception as e:
        await message.answer('Error while downloading file')
        return

    file = await bot.get_file(file_obj.file_id)

    await bot.download_file(file.file_path, file_obj.file_name)

    agenda = FSInputFile(file_obj.file_name, filename=file_obj.file_name)

    await message.answer_document(agenda)

if __name__ == "__main__":
    dp.run_polling(bot)