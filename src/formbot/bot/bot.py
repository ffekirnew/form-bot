from telebot import TeleBot, custom_filters
from telebot.states.sync.middleware import StateMiddleware
from telebot.storage import StatePickleStorage
from telebot.types import Update

from config import Settings
from formbot.bot.forms.y2024.fifth_year_form import FifthYear2024FormHandler
from formbot.bot.init_handler import InitHandler


class Bot:
    def __init__(self, config: Settings) -> None:
        self._config = config
        self._bot = TeleBot(
            self._config.bot_token.get_secret_value(),
            state_storage=StatePickleStorage("./.botstates/state.pkl"),
            use_class_middlewares=True,
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

    def start(self) -> None:
        for handler in self._form_handlers:
            handler.start()
        self._init_handler.start()

        self._setup_filters()
        self._setup_middlewares()

        if self._config.env == "prod":
            self._bot.remove_webhook()
            self._bot.set_webhook(self._config.webhook_url)
            self._bot.run_webhooks()

        else:
            self._bot.delete_webhook()
            self._bot.polling()

    def _setup_filters(self) -> None:
        self._bot.add_custom_filter(custom_filters.StateFilter(self._bot))
        self._bot.add_custom_filter(custom_filters.IsDigitFilter())
        self._bot.add_custom_filter(custom_filters.TextMatchFilter())

    def _setup_middlewares(self) -> None:
        self._bot.setup_middleware(StateMiddleware(self._bot))

    def process_new_updates(self, updates: list[Update]) -> None:
        self._bot.process_new_updates(updates)
