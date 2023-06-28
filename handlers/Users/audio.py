from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from loader import dp, bot
from states.download import Download

from pytube import YouTube
import os
import uuid

def download_video(url, type='audio'):
    yt = YouTube(url)
    audio_id = uuid.uuid4().fields[-1]
    if type == 'audio':
        yt.streams.filter(only_audio=True).first().download("audio", f"{audio_id}.mp3")
        return f"{audio_id}.mp3"
    elif type == 'video':
        return f"{audio_id}.mp4"
    
@dp.message_handler(Command("audio"))
async def start_dow(message: types.Message):
    await message.answer("Paste URL of the video and get its audio version")
    await Download.download.set()

@dp.message_handler(state=Download.download)
async def download(message: types.Message, state: FSMContext):
    title = download_video(message.text)
    audio = open(f'audio/{title}', 'rb')
    await message.answer(text="Download is complete. Here's your audio")
    try:
        await bot.send_audio(message.chat.id, audio)
        await bot.send_message(message.chat.id, text='')
    except:
        await message.answer(text="File is too large")
    os.remove(f'audio/{title}')
    await state.finish()