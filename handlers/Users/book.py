from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from loader import dp, bot
from db.connect import Database
from states.upload import Upload
import uuid

def upload_book_db(book_id, book_name, location):
    db = Database()
    db_conn = db.connect()
    query = f"INSERT INTO books (id, book_name, location) VALUES ({book_id}, '{book_name}', '{location}') RETURNING id"
    if db_conn:
        try:
            return db.query_db(query, db_conn)
        except:
            print(f"Incorrect query: {query}")
            return None
    else:
        print("Can't connect to database")
        return None
            

@dp.message_handler(Command("upload"))
async def start_upload_file(message: types.Message):
    await message.answer("Drop a book file to upload")
    await Upload.upload.set()

@dp.message_handler(state=Upload.upload, content_types=['any'])
async def upload_file(message: types.Message, state: FSMContext):
    if message.document: # Checks if the file user dropped is actually a document
        file_id = message.document.file_id
        book_name = message.document.file_name
        book_id = uuid.uuid4().fields[-1]
        location = f"/home/focus/project2/books/{book_id}"
        try:
            await bot.download_file_by_id(file_id, location) # Downloads a file from telegram
        except:
            await message.answer("Error has ocurred while uploading file")
        if upload_book_db(book_id, book_name, location): # Adds book to db
                await message.answer("The book has successfuly uploaded")
        else:
            await message.answer("The book was not added to database")
    else:
        await message.answer("This is not a book! Try /upload again")
    await state.finish() # Unsets the state Upload in any case
    
    

    