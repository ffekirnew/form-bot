from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StatePickleStorage
from telebot.states.asyncio.middleware import StateMiddleware
from telebot.types import Update

from config import Settings
from formbot.bot.forms.y2024.fifth_year_form import FifthYear2024FormHandler
from formbot.bot.init_handler import InitHandler


class Bot:
    def __init__(self, config: Settings) -> None:
        self._config = config
        self._bot = AsyncTeleBot(
            self._config.bot_token.get_secret_value(),
            state_storage=StatePickleStorage(".botstate/states.pkl"),
        )

        self._form_handlers = [
            FifthYear2024FormHandler(self._bot, "Fifth Year 2024 Form"),
        ]
        self._init_handler = InitHandler(
            self._bot,
            [handler.form_name for handler in self._form_handlers],
            config.bot_name,
        )

    @property
    def token(self) -> str:
        return self._bot.token

    async def start(self) -> None:
        for handler in self._form_handlers:
            handler.start()
        self._init_handler.start()

        self._setup_filters()
        self._setup_middleware()

        if self._config.env == "prod":
            await self._bot.remove_webhook()
            await self._bot.set_webhook(self._config.webhook_url)
            await self._bot.run_webhooks()

        else:
            await self._bot.delete_webhook()
            await self._bot.polling()

    def _setup_filters(self) -> None:
        self._bot.add_custom_filter(asyncio_filters.IsDigitFilter())
        self._bot.add_custom_filter(asyncio_filters.TextMatchFilter())
        self._bot.add_custom_filter(asyncio_filters.StateFilter(self._bot))

    def _setup_middleware(self) -> None:
        self._bot.setup_middleware(StateMiddleware(self._bot))

    async def process_new_updates(self, updates: list[Update]) -> None:
        await self._bot.process_new_updates(updates)
