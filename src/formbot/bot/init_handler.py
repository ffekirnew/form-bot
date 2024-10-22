from telebot import TeleBot
from telebot.states.sync.context import StateContext
from telebot.types import Message

from formbot.bot.utils import BotState, Handler
from formbot.bot.utils.keyboards import make_column_keyboard

INTRO = "Select the form you want to fill from the options below."


class InitHandler(Handler):
    def __init__(
        self,
        bot: TeleBot,
        forms: list[str],
        bot_name: str,
    ) -> None:
        super().__init__(bot)
        self._forms = forms
        self._bot_name = bot_name

    def start(self):
        self.register()

    def register(self):
        self.register_handler(
            self._start,
            commands=["start"],
        )

    def _start(self, message: Message, state: StateContext) -> None:
        assert message.from_user is not None

        cid = message.chat.id

        with state.data() as data:  # type: ignore
            registered = data.get("registered", False)

            if not registered:
                self.send_message(
                    cid,
                    f"Hello, I'm {self._bot_name}!\n\n{INTRO}",
                    reply_markup=make_column_keyboard(self._forms),
                )

            else:
                self.send_message(
                    cid,
                    f"Hi {message.from_user.first_name}, I'm {self._bot_name}!\n\n{INTRO}",
                    reply_markup=make_column_keyboard(self._forms),
                )

            state.set(BotState.init)
