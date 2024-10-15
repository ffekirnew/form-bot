from telebot.asyncio_filters import SimpleCustomFilter

from formbot.bot.utils.generic_helpers import is_valid_email


class IsEmailFilter(SimpleCustomFilter):
    key = "is_email"

    async def check(self, message):
        return is_valid_email(message.text.isdigit())
