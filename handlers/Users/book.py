from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from loader import dp, bot
from db.database import Database
import os
from states.upload import Upload
import uuid
from PyPDF4 import PdfFileReader

def query_db(query):
    db = Database()
    db_conn = db.connect()
    if db_conn:
        try:
            return db.query_db(query, db_conn)
        except:
            print(f"Incorrect query: {query}")
    else:
        print("Can't connect to database")
            

@dp.message_handler(Command("upload"))
async def set_upload_state(message: types.Message):
    await message.answer("Drop a book file to upload")
    await Upload.upload.set() # Sets the state to Upload 

@dp.message_handler(state=Upload.upload, content_types=['any']) # Triggers when state is Upload
async def upload_file(message: types.Message, state: FSMContext):
    if message.document: # Checks if the file user dropped is actually a document
        file_id = message.document.file_id
        book_name = message.document.file_name
        book_id = uuid.uuid4().fields[-1]
        location = f"/home/focus/project2/books/{book_id}"
        query = f"INSERT INTO books (id, book_name, location) VALUES ({book_id}, '{book_name}', '{location}') RETURNING id"
        try:
            await bot.download_file_by_id(file_id, location) # Downloads a file from telegram
        except:
            await message.answer("Error has ocurred while uploading file")
        
        if os.path.exists(location):
            if query_db(query): # Adds book to db
                    await message.answer("The book has successfuly uploaded")
            else:
                await message.answer("The book was not added to database")
                os.remove(location)
    else:
        await message.answer("This is not a book! Try /upload again")
    await bot.delete_message(message.chat.id, message.message_id)
    await state.finish() # Unsets the state Upload in any case

def get_pdf_info(location):
    with open(location, 'rb') as book:
        pdf = PdfFileReader(book, strict=False)
        info = pdf.getDocumentInfo()
        return info


@dp.message_handler(Command("list"))
async def list_books(message: types.Message):
    books_list = ""
    query = "SELECT location FROM books"
    books_location = query_db(query)
    for book_loc in books_location:
        book_info = get_pdf_info(str(book_loc).strip("()',"))
        books_list += f"{book_info.title}\n"
    await message.answer(books_list)

    