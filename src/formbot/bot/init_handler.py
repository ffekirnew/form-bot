from telebot.states.asyncio.context import AsyncTeleBot, Message, StateContext

from formbot.bot.utils import BotState, Handler
from formbot.bot.utils.keyboards import make_column_keyboard, register_keyboard

NAME = "5 Kilo Gibi Gubae Forms Bot"
INTRO = "Select the form you want to fill from the options below."


class InitHandler(Handler):
    def __init__(self, bot: AsyncTeleBot, forms: list[str]) -> None:
        super().__init__(bot)
        self._forms = forms

    def start(self):
        self.register()

    def register(self):
        self.register_handler(
            self._start,
            commands=["start"],
        )

    async def _start(self, message: Message, state: StateContext) -> None:
        assert message.from_user is not None

        cid = message.chat.id

        async with state.data() as data:  # type: ignore
            registered = data.get("registered", False)

            if not registered:
                await self.send_message(
                    cid,
                    f"Hello, I'm {NAME}!\n\n{INTRO}",
                    reply_markup=make_column_keyboard(self._forms),
                )

            else:
                await self.send_message(
                    cid,
                    f"Hi {message.from_user.first_name}, I'm {NAME}!\n\n{INTRO}",
                    reply_markup=make_column_keyboard(self._forms),
                )

            await state.set(BotState.init)
