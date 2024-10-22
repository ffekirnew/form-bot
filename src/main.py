from dotenv import load_dotenv

from config import Settings
from formbot import Bot


def main():
    load_dotenv(override=True)
    config = Settings()  # type: ignore
    bot = Bot(config)
    bot.start()


if __name__ == "__main__":
    main()
