from abc import abstractmethod
from typing import Callable

from telebot import State, TeleBot
from telebot.types import ABC, InlineKeyboardMarkup, ReplyKeyboardMarkup


class Handler(ABC):
    def __init__(self, bot: TeleBot) -> None:
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

    def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    ) -> None:
        self._bot.send_message(chat_id, text, reply_markup=reply_markup)

    def set_state(self, uid: int, state: State, cid: int) -> None:
        self._bot.set_state(uid, state, cid)

    def retrieve_data(self, uid: int, cid: int) -> dict | None:
        return self._bot.retrieve_data(uid, cid)

    def add_data(self, uid: int, cid: int, **args) -> None:
        self._bot.add_data(uid, cid, **args)


class FormHandler(Handler):
    def __init__(self, bot: TeleBot, form_name: str) -> None:
        super().__init__(bot)
        self._form_name = form_name

    @property
    def form_name(self):
        """The form_name property."""
        return self._form_name
