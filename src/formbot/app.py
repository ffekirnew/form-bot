from formbot.bot import Bot


class App:
    def __init__(self) -> None:
        self._bot = Bot()

    async def start(self, is_bot_start: bool = True) -> None:
        if is_bot_start:
            await self._bot.start()

    @property
    def bot(self):
        return self._bot
