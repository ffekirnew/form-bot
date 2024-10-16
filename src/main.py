from dotenv import load_dotenv

from config import Settings
from formbot import Bot


async def main():
    load_dotenv(override=True)
    config = Settings()  # pyright: ignore

    bot = Bot(config, webhook=True)
    await bot.start()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
