from telebot import TeleBot
from telebot.states.sync.context import StateContext
from telebot.types import Message

from formbot.bot.forms.y2024.third_year_form.form_resources import (
    SERVICE_DEPARTMENTS,
    Student,
    get_department_names,
)
from formbot.bot.forms.y2024.third_year_form.form_service import FormService
from formbot.bot.forms.y2024.third_year_form.form_states import ThirdYearFormStates
from formbot.bot.utils import BotState, FormHandler
from formbot.bot.utils.generic_helpers import (
    is_valid_email,
    is_valid_ethiopian_phone_number,
    standardize_phone_number,
)
from formbot.bot.utils.keyboards import (
    make_column_keyboard,
    make_row_keyboard,
    make_share_contact_keyboard,
)
from formbot.bot.utils.logger import get_logger

UNIVERSITY_DEPARTMENT_PROMPT = "Please select your university department."
UNIVERSITY_DEPARTMENT_STREAM_PROMPT = "Please select your stream."
UNIVERSITY_DEPARTMANET_SECTION_PROMPT = "Please share your section."
FULL_NAME_PROMPT = "Please share your full name."
PHONE_NUMBER_PROMPT = "Please share your phone number."
PHONE_NUMBER_INVALID_PROMPT = "Invalid phone number. Please share a valid phone number. Should start with one of: +251, 251, 07, 09. Or you can share your contact."
EMAIL_PROMPT = "Please share your email."
EMAIL_INVALID_PROMPT = "Invalid email. Please share a valid email."
FINAL_MESSAGE = "Thank you for sharing your information."
SERVICE_DEPARTMENT_PROMPT = "Please share your service class."

LOG = get_logger()


class ThirdYear2024FormHandler(FormHandler):
    def __init__(self, bot: TeleBot, form_name: str) -> None:
        super().__init__(bot, form_name)

    def start(self) -> None:
        return self.register()

    def register(self) -> None:
        self.register_handler(
            self._init,
            state=BotState.init,
            text=[self._form_name],
        )
        self.register_handler(
            self._university_department,
            state=ThirdYearFormStates.waiting_for_university_department,
        )
        self.register_handler(
            self._name,
            state=ThirdYearFormStates.waiting_for_name,
        )
        self.register_handler(
            self._phone,
            state=ThirdYearFormStates.waiting_for_phone_number,
        )
        self.register_handler(
            self._phone,
            state=ThirdYearFormStates.waiting_for_phone_number,
            content_types=["contact"],
        )
        self.register_handler(
            self._service_department,
            state=ThirdYearFormStates.waiting_for_service_department,
        )
        self.register_handler(
            self._email,
            state=ThirdYearFormStates.waiting_for_email,
        )

    def _init(self, message: Message, state: StateContext) -> None:
        cid = message.chat.id

        state.set(ThirdYearFormStates.waiting_for_university_department)
        self.send_message(
            cid,
            UNIVERSITY_DEPARTMENT_PROMPT,
            make_row_keyboard(get_department_names(), items_per_row=1),
        )

    def _university_department(self, message: Message, state: StateContext) -> None:
        print("here")
        cid, department = message.chat.id, message.text

        assert department is not None
        state.add_data(department=department)

        state.set(ThirdYearFormStates.waiting_for_name)
        self.send_message(
            cid,
            FULL_NAME_PROMPT,
        )

    def _name(self, message: Message, state: StateContext) -> None:
        cid, name = message.chat.id, message.text
        assert name is not None

        state.add_data(name=name)

        state.set(ThirdYearFormStates.waiting_for_phone_number)
        self.send_message(
            cid,
            PHONE_NUMBER_PROMPT,
            reply_markup=make_share_contact_keyboard("Share your contact"),
        )

    def _phone(self, message: Message, state: StateContext) -> None:
        cid = message.chat.id

        phone = None
        if message.contact is not None:
            phone = message.contact.phone_number

        if phone is None and is_valid_ethiopian_phone_number(message.text):  # type: ignore
            phone = message.text

        if phone is not None:
            state.add_data(phone_number=standardize_phone_number(phone))

            state.set(ThirdYearFormStates.waiting_for_service_department)
            self.send_message(
                cid,
                SERVICE_DEPARTMENT_PROMPT,
                make_column_keyboard(SERVICE_DEPARTMENTS),
            )
        else:
            self.send_message(
                cid,
                PHONE_NUMBER_INVALID_PROMPT,
                reply_markup=make_share_contact_keyboard("Share your contact"),
            )

    def _service_department(self, message: Message, state: StateContext) -> None:
        cid = message.chat.id

        department = message.text
        assert department is not None

        if department not in SERVICE_DEPARTMENTS:
            self.send_message(cid, SERVICE_DEPARTMENT_PROMPT)
            return

        state.add_data(service_department=department)
        state.set(ThirdYearFormStates.waiting_for_email)
        self.send_message(
            cid,
            EMAIL_PROMPT,
        )

    def _email(self, message: Message, state: StateContext) -> None:
        cid, email = message.chat.id, message.text

        assert email is not None

        if not is_valid_email(email):
            self.send_message(cid, EMAIL_INVALID_PROMPT)
            return

        with state.data() as data:  # type: ignore
            student: Student = {
                "name": data.get("name"),
                "phone_number": data.get("phone_number"),
                "email": email,
                "department": data.get("department"),
                "stream": data.get("stream", "-"),
                "section": data.get("section", "-"),
                "service_department": data.get("service_department"),
            }

        service = FormService()
        service.insert(student)
        LOG.info(f"Inserted a third year student: {student}")

        state.add_data(registered=True)
        state.set(BotState.init)
        self.send_message(
            cid,
            FINAL_MESSAGE,
        )
