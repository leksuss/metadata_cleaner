import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from libmat2 import parser_factory

import bot_logger
from config import config

dp = Dispatcher()

def allowed_file(filename):
    _, _, ext = filename.rpartition('.')
    return ext.lower() in config['ALLOWED_EXTENSIONS']

@dp.message(commands=["start"])
async def command_start_handler(message: types.message):
    await message.answer(f'''
Привет! Я чищу метадату в файлах. Поддерживаются следующие форматы:
{', '.join(config['ALLOWED_EXTENSIONS'])}
Папки и архивы пока не работают, но можно кидать сразу несколько файлов! 
        '''
    )

@dp.message()
async def prepare_message(message: types.document):

    user_id = message.from_user.id

    try:
        file_obj = message.document
        file = await bot.get_file(file_obj.file_id)

    except Exception as e:
        await message.answer('Пожалуйста, пришлите файл')
        logger.warning(f"user_id:{user_id} - User send not a file")
        return

    if not allowed_file(file_obj.file_name):
        await message.answer('Данный тип файлов не поддерживается. Поддерживаются: ' + ', '.join(config['ALLOWED_EXTENSIONS']))
        logger.warning(f"user_id:{user_id} - User send wrong file format")
        return

    local_filepath = os.path.join(config['UPLOAD_FOLDER'], file_obj.file_name)
    try:
        await bot.download_file(file.file_path, local_filepath)
    except Exception:
        await message.answer('Проблема с сохранением файла на сервере, обратитесь к разработчику')
        logger.error(f"user_id:{user_id} - Can't save file. Permissions, wrong path, UPLOAD_FOLDER does not exist?")
        return

    try:
        parser, mime = parser_factory.get_parser(local_filepath)

        parser.lightweight_cleaning = True
        parser.remove_all()
        os.rename(parser.output_filename, local_filepath)
        output_file = FSInputFile(local_filepath)
        await message.answer_document(output_file)
        logger.info(f"user_id:{user_id} - Successfully clean file metadata")

    except ValueError:
        await message.answer('Ошибка чистки метаданных. Неверный формат файла?')
        logger.error(f"user_id:{user_id} - Can't clean file metadata. Wrong file format or something with mat2")
        return

if __name__ == "__main__":
    load_dotenv()
    bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
    logger = bot_logger.error_logger_in_file(__name__)
    dp.run_polling(bot)