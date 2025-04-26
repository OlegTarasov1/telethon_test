from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from telethon_client.telethon_functions import is_spammed_distributor
from .additional_functions import (
    arch_to_folder,
    clear_temp_files,
    get_file_names_from_folder
)
from asyncio import Semaphore
import pathlib
import aiofiles
import json

spambot_cheack = Router()

@spambot_cheack.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("well this works...")


@spambot_cheack.message(Command("check"))
async def check_spam(msg: Message):
    # clear_temp_files("./media/src")
    # clear_temp_files("./media/new_sessions")
    
    if msg.document:
        file_info = await msg.bot.get_file(msg.document.file_id)
        file_path = file_info.file_path
        file_name = msg.document.file_name
        file = await msg.bot.download_file(file_path)

        save_path = f"./media/src/{file_name}"
        async with aiofiles.open(save_path, "wb") as f:
            await f.write(file.read())

        await msg.answer("файл сохранён.")
        save_path = await arch_to_folder(save_path)
        await msg.answer("файл разархивирован..")
        json_list = await get_file_names_from_folder(save_path)
        print(json_list)
        await msg.answer("json лист должен быть в логах...")

        counter = 0
        for i in json_list:
            resp = await is_spammed_distributor(i)
            if resp and resp.lower() != "incorrect session":
                counter += 1
            elif resp.lower() == "incorrect session":
                await msg.answer("что-то не так с файлом сессии")
            print(counter)
        
        await msg.answer(f"не заспамленно было {counter} аккаунтов!")
        

    else:
        await msg.answer("вы забыли отправить файл")


# @spambot_cheack.message(Command("unzip"))
# async def unzip_folder(msg: Message):
#     resp = await arch_to_folder("./media/src/new_zip_test.zip")
#     if resp != "Unsupported file type":
#         await msg.answer(f"всё разархивировано в папку: {resp}!")
#     else:
#         await msg.answer("не так что-то...")