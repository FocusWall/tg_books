from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("help", "Help"),
            types.BotCommand("audio", "Get audio from youtube"),
            types.BotCommand("upload", "To upload a file"),
            types.BotCommand("list", "To list all the books"),
        ]
    )