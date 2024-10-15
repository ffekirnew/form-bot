from telebot.states import State, StatesGroup


class FormStates(StatesGroup):
    init = State()
    waiting_for_university_department = State()
    waiting_for_university_department_stream = State()
    waiting_for_university_department_section = State()
    waiting_for_name = State()
    waiting_for_phone_number = State()
    waiting_for_email = State()
