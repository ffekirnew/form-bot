from dotenv import load_dotenv

from config import Settings
from formbot import Bot

load_dotenv(override=True)
config = Settings()  # type: ignore


async def main():
    bot = Bot(config)
    await bot.start()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
