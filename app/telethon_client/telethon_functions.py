from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import asyncio
import aiofiles
import json
import re


semaphore = asyncio.Semaphore(1)

async def is_spammed_distributor(file_name: str) -> bool | str:
    async with aiofiles.open(
        f"./media/src/{file_name}",
        mode = "r",
        encoding = "utf-8"
    ) as file:
        content = await file.read()
        content_dict = json.loads(content)

    async with semaphore:
        resp = await is_spammed(content_dict)
    return resp


async def is_spammed(creds: dict) -> bool | str:
    phone = creds.get("phone")

    client_session = TelegramClient(
        f'media/src/{creds.get("session_file")}',
        api_id = creds.get("app_id"),
        api_hash = creds.get("app_hash")
    )
    await client_session.connect()

    new_client_session = TelegramClient(
        f'media/new_sessions/{creds.get("session_file")}',
        api_id = creds.get("app_id"),
        api_hash = creds.get("app_hash"),
        device_model = creds.get("device_model"),
        system_version = creds.get("system_version"),
        lang_code = creds.get("lang_pack"),
        system_lang_code = creds.get("system_lang_pack")
    )
    await new_client_session.connect()


    await new_client_session.send_code_request(phone)
    
    try:
        response = await client_session.get_messages("42777", limit = 1)
    except:
        return "Incorrect session"
    auth_code = re.sub(r'\D', '', response[0].text)

    await client_session.disconnect()
    
    try:
        await new_client_session.sign_in(phone, auth_code)
    except SessionPasswordNeededError:
        await new_client_session.sign_in(password = creds.get("twoFA"))

    await new_client_session.send_message("@SpamBot", "/start")
    response = await new_client_session.get_messages("@SpamBot", limit = 1)
    await new_client_session.disconnect()
    if response[0].text == "Ваш аккаунт свободен от каких-либо ограничений.":
        return True
    else:
        return False

