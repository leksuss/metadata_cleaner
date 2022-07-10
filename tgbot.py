import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from libmat2 import parser_factory



UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = {'pdf'}

dp = Dispatcher()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dp.message(commands=["start"])
async def command_start_handler(message: types.message):
    await message.answer(f'''
Привет! Я чищу метадату в файлах. Поддерживаются следующие форматы:
{', '.join(ALLOWED_EXTENSIONS)}
Папки и архивы пока не работают, но можно кидать сразу несколько файлов! 
        '''
    )


@dp.message()
async def prepare_message(message: types.document):

    try:
        file_obj = message.document
        file = await bot.get_file(file_obj.file_id)

    except Exception as e:
        await message.answer('Пожалуйста, пришлите файл')
        logger.info("User send not a file")
        return

    if not allowed_file(file_obj.file_name):
        await message.answer('Данный тип файлов не поддерживается. Поддерживаются: ' + ', '.join(ALLOWED_EXTENSIONS))
        logger.info("User send wrong file format")
        return


    local_filepath = UPLOAD_FOLDER + file_obj.file_name
    try:
        await bot.download_file(file.file_path, local_filepath)
    except Exception:
        await message.answer('Проблема с сохранением файла на сервере, обратитесь к разработчику')
        logger.error("Can't save file on server. Permissions, wrong path, UPLOAD_FOLDER does not exist?")
        return

    try:
        parser, mime = parser_factory.get_parser(local_filepath)

        parser.lightweight_cleaning = True
        parser.remove_all()
        os.rename(parser.output_filename, local_filepath)
        output_file = FSInputFile(local_filepath)
        await message.answer_document(output_file)

    except ValueError:
        await message.answer('Ошибка чистки метаданных. Неверный формат файла?')
        logger.warning("Can't clean metadata. Wrong file format or something with mat2")
        return


if __name__ == "__main__":
    load_dotenv()
    bot = Bot(os.getenv('TOKEN'))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")
    dp.run_polling(bot)