from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from loader import dp, bot
from states.upload import Upload

@dp.message_handler(Command("upload"))
async def start_upload_file(message: types.Message):
    await message.answer("Drop a book file to upload")
    await Upload.upload.set()

@dp.message_handler(state=Upload.upload, content_types=['any'])
async def upload_file(message: types.Message, state: FSMContext):
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name

        await message.answer("Worked")
        try:
            await bot.download_file_by_id(file_id, f"/home/focus/project2/files/{file_name}")
        except:
            await message.answer("Error has ocurred while uploading file")
    else:
        await message.answer("This is not a book! Try /upload again")
    await state.finish()