from abc import abstractmethod
from typing import Callable

from telebot.async_telebot import AsyncTeleBot
from telebot.types import ABC, InlineKeyboardMarkup, ReplyKeyboardMarkup


class Handler(ABC):
    def __init__(self, bot: AsyncTeleBot) -> None:
        self._bot = bot

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def register(self) -> None: ...

    def register_handler(
        self,
        handler_function: Callable,
        **args,
    ) -> None:
        self._bot.register_message_handler(handler_function, **args)

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    ) -> None:
        await self._bot.send_message(chat_id, text, reply_markup=reply_markup)


class FormHandler(Handler):
    def __init__(self, bot: AsyncTeleBot, form_name: str) -> None:
        super().__init__(bot)
        self._form_name = form_name

    @property
    def form_name(self):
        """The form_name property."""
        return self._form_name
