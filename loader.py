from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = '6080990250:AAGBI-fMu_wWMy6QMV5C6rIc7OARVv342d8'

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)