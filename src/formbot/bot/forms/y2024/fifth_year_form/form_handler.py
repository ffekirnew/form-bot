from telebot.states.asyncio.context import AsyncTeleBot, StateContext
from telebot.types import Message

from formbot.bot.forms.y2024.fifth_year_form.form_resources import (
    Student,
    get_department_names,
    get_department_stream_names,
    get_sections,
)
from formbot.bot.forms.y2024.fifth_year_form.form_states import FormStates
from formbot.bot.utils import BotState, FormHandler
from formbot.bot.utils.keyboards import make_row_keyboard, make_share_contact_keyboard

UNIVERSITY_DEPARTMENT_PROMPT = "Please share your university department."
UNIVERSITY_DEPARTMENT_STREAM_PROMPT = "Please share your university department stream."
UNIVERSITY_DEPARTMANET_SECTION_PROMPT = (
    "Please share your university department section."
)
FULL_NAME_PROMPT = "Please share your full name."
PHONE_NUMBER_PROMPT = "Please share your phone number."
EMAIL_PROMPT = "Please share your email."


class FifthYear2024FormHandler(FormHandler):
    def __init__(self, bot: AsyncTeleBot, form_name: str) -> None:
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
            state=FormStates.waiting_for_university_department,
        )
        self.register_handler(
            self._university_department_stream,
            state=FormStates.waiting_for_university_department_stream,
        )
        self.register_handler(
            self._university_department_section,
            state=FormStates.waiting_for_university_department_section,
        )
        self.register_handler(
            self._name,
            state=FormStates.waiting_for_name,
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
            make_row_keyboard(get_department_names()),
        )

    async def _university_department(
        self, message: Message, state: StateContext
    ) -> None:
        cid, department = message.chat.id, message.text

        assert department is not None
        await state.add_data(department=department)

        if get_department_stream_names(department):
            await state.set(FormStates.waiting_for_university_department_stream)
            await self.send_message(
                cid,
                UNIVERSITY_DEPARTMENT_STREAM_PROMPT,
                make_row_keyboard(get_department_stream_names(department)),
            )

        else:
            await state.set(FormStates.waiting_for_university_department_section)
            await self.send_message(
                cid,
                UNIVERSITY_DEPARTMANET_SECTION_PROMPT,
                make_row_keyboard(get_sections(department)),
            )

    async def _university_department_stream(
        self, message: Message, state: StateContext
    ) -> None:
        cid, stream = message.chat.id, message.text

        assert stream is not None
        await state.add_data(stream=stream)

        async with state.data() as data:  # type: ignore
            department = data.get("department")
            await state.set(FormStates.waiting_for_university_department_section)
            await self.send_message(
                cid,
                UNIVERSITY_DEPARTMANET_SECTION_PROMPT,
                make_row_keyboard(get_sections(department, stream)),
            )

    async def _university_department_section(
        self, message: Message, state: StateContext
    ) -> None:
        cid, section = message.chat.id, message.text

        assert section is not None
        await state.add_data(section=section)

        await state.set(FormStates.waiting_for_name)
        await self.send_message(cid, FULL_NAME_PROMPT)

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

        assert message.contact is not None
        phone = message.contact.phone_number

        await state.add_data(phone_number=phone)

        await state.set(FormStates.waiting_for_email)
        await self.send_message(
            cid,
            EMAIL_PROMPT,
        )

    async def _email(self, message: Message, state: StateContext) -> None:
        cid, email = message.chat.id, message.text

        assert email is not None

        async with state.data() as data:  # type: ignore
            self.finalize(
                {
                    "name": data.get("name"),
                    "phone_number": data.get("phone_number"),
                    "email": email,
                    "department": data.get("department"),
                    "stream": data.get("stream"),
                    "section": data.get("section"),
                }
            )
            await state.set(BotState.init)
            await self.send_message(
                cid,
                "Thank you for sharing your information.",
            )

    def finalize(self, student: Student) -> None:
        print(student)
