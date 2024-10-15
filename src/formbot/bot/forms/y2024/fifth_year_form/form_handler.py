from telebot.states.asyncio.context import AsyncTeleBot, StateContext
from telebot.types import Message

from formbot.bot.forms.y2024.fifth_year_form.form_resources import (
    Student,
    get_department_names,
    get_department_stream_names,
    get_sections,
)
from formbot.bot.forms.y2024.fifth_year_form.form_service import FormService
from formbot.bot.forms.y2024.fifth_year_form.form_states import FormStates
from formbot.bot.utils import BotState, FormHandler
from formbot.bot.utils.generic_helpers import (
    is_valid_email,
    is_valid_ethiopian_phone_number,
    standardize_phone_number,
)
from formbot.bot.utils.keyboards import make_row_keyboard, make_share_contact_keyboard

UNIVERSITY_DEPARTMENT_PROMPT = "Please select your university department."
UNIVERSITY_DEPARTMENT_STREAM_PROMPT = "Please select your stream."
UNIVERSITY_DEPARTMANET_SECTION_PROMPT = "Please share your section."
FULL_NAME_PROMPT = "Please share your full name."
PHONE_NUMBER_PROMPT = "Please share your phone number."
PHONE_NUMBER_INVALID_PROMPT = "Invalid phone number. Please share a valid phone number. Should start with one of: +251, 251, 07, 09. Or you can share your contact."
EMAIL_PROMPT = "Please share your email."
EMAIL_INVALID_PROMPT = "Invalid email. Please share a valid email."
FINAL_MESSAGE = "Thank you for sharing your information."


class FifthYear2024FormHandler(FormHandler):
    def __init__(self, bot: AsyncTeleBot, form_name: str) -> None:
        super().__init__(bot, form_name)
        self._service = FormService()

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
            state=FormStates.waiting_for_university_department,
        )
        self.register_handler(
            self._name,
            state=FormStates.waiting_for_name,
        )
        self.register_handler(
            self._phone,
            state=FormStates.waiting_for_phone_number,
        )
        self.register_handler(
            self._phone,
            state=FormStates.waiting_for_phone_number,
            content_types=["contact"],
        )
        self.register_handler(
            self._email,
            state=FormStates.waiting_for_email,
        )

    async def _init(self, message: Message, state: StateContext) -> None:
        cid = message.chat.id

        await state.set(FormStates.waiting_for_university_department)
        await self.send_message(
            cid,
            UNIVERSITY_DEPARTMENT_PROMPT,
            make_row_keyboard(get_department_names(), items_per_row=1),
        )

    async def _university_department(
        self, message: Message, state: StateContext
    ) -> None:
        cid, department = message.chat.id, message.text

        assert department is not None
        await state.add_data(department=department)

        await state.set(FormStates.waiting_for_name)
        await self.send_message(
            cid,
            FULL_NAME_PROMPT,
        )

    async def _name(self, message: Message, state: StateContext) -> None:
        cid, name = message.chat.id, message.text
        assert name is not None

        await state.add_data(name=name)

        await state.set(FormStates.waiting_for_phone_number)
        await self.send_message(
            cid,
            PHONE_NUMBER_PROMPT,
            reply_markup=make_share_contact_keyboard("Share your contact"),
        )

    async def _phone(self, message: Message, state: StateContext) -> None:
        cid = message.chat.id

        phone = None
        if message.contact is not None:
            phone = message.contact.phone_number

        if phone is None and is_valid_ethiopian_phone_number(message.text):  # type: ignore
            phone = message.text

        if phone is not None:
            await state.add_data(phone_number=standardize_phone_number(phone))

            await state.set(FormStates.waiting_for_email)
            await self.send_message(
                cid,
                EMAIL_PROMPT,
            )
        else:
            await self.send_message(
                cid,
                PHONE_NUMBER_INVALID_PROMPT,
                reply_markup=make_share_contact_keyboard("Share your contact"),
            )

    async def _email(self, message: Message, state: StateContext) -> None:
        cid, email = message.chat.id, message.text

        assert email is not None

        if not is_valid_email(email):
            await self.send_message(cid, EMAIL_INVALID_PROMPT)
            return

        async with state.data() as data:  # type: ignore
            self.finalize(
                {
                    "name": data.get("name"),
                    "phone_number": data.get("phone_number"),
                    "email": email,
                    "department": data.get("department"),
                    "stream": data.get("stream", "-"),
                    "section": data.get("section", "-"),
                }
            )
            await state.set(BotState.init)
            await self.send_message(
                cid,
                FINAL_MESSAGE,
            )

    def finalize(self, student: Student) -> None:
        self._service.insert(student)
