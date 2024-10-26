import logging
import asyncio
from db import create_table
from bot import dp, bot

logging.basicConfig(level=logging.INFO)

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())