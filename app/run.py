from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from routers.spambot_router import spambot_cheack
import asyncio
import os



async def main():
    load_dotenv()
    bot = Bot(token = os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    
    dp.include_router(spambot_cheack)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('quit manually')
    except Exception as e:
        print(e)
