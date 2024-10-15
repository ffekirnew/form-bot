"""Filter"""

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import Message

from formbot.bot.utils.generic_helpers import is_valid_ethiopian_phone_number


class IsPhoneNumberFilter(SimpleCustomFilter):
    key = "is_phone_number"

    def __init__(self, bot: AsyncTeleBot):
        self.bot = bot

    async def check(self, message: Message) -> bool:
        return is_valid_ethiopian_phone_number(message.text)
