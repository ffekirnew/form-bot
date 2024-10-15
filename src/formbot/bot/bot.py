from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StatePickleStorage
from telebot.states.asyncio.middleware import StateMiddleware

from formbot.bot.forms.y2024.fifth_year_form import FifthYear2024FormHandler
from formbot.bot.init_handler import InitHandler


class Bot:
    def __init__(self) -> None:
        self._bot = AsyncTeleBot(
            "7340398878:AAGarQcbjKdGayZogWAeXMggg2PEtTH8x2s",
            state_storage=StatePickleStorage(".botstate/states.pkl"),
        )

        self._form_handlers = [
            FifthYear2024FormHandler(self._bot, "Fifth Year 2024 Form"),
        ]
        self._init_handler = InitHandler(
            self._bot,
            [handler.form_name for handler in self._form_handlers],
        )

    async def start(self) -> None:
        for handler in self._form_handlers:
            handler.start()
        self._init_handler.start()

        self._setup_filters()
        self._setup_middleware()
        await self._bot.remove_webhook()
        await self._bot.polling()

    def _setup_filters(self) -> None:
        self._bot.add_custom_filter(asyncio_filters.IsDigitFilter())
        self._bot.add_custom_filter(asyncio_filters.IsEmailFilter())
        self._bot.add_custom_filter(asyncio_filters.TextMatchFilter())
        self._bot.add_custom_filter(asyncio_filters.StateFilter(self._bot))

    def _setup_middleware(self) -> None:
        self._bot.setup_middleware(StateMiddleware(self._bot))
