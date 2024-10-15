from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def register_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    items = [
        list(map(KeyboardButton, ["Register", "Help"])),
        list(map(KeyboardButton, ["About"])),
    ]

    for row in items:
        keyboard.add(*row)

    return keyboard


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keyboard.add(*[KeyboardButton(text=item) for item in items])

    return keyboard


def make_column_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keyboard.add(*[KeyboardButton(text=item) for item in items])

    return keyboard


def make_share_contact_keyboard(prompt: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keyboard.add(KeyboardButton(prompt, request_contact=True))

    return keyboard
