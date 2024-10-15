from formbot.bot.forms.y2024.fifth_year_form.form_resources import Student
from formbot.storage import SqliteDb

TABLE_NAME = "students"

CREATE_TABLE_QUERY = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    department TEXT,
    stream TEXT,
    section TEXT
)
"""

INSERT_QUERY = f"""
INSERT INTO {TABLE_NAME} (department, stream, section, name, phone, email) VALUES (?, ?, ?, ?, ?, ?)
"""


class FormService:
    def __init__(self) -> None:
        self._db = SqliteDb("data/fifth_year_2024.db")
        self._create_table()

    def insert(self, student: Student) -> None:
        self._db.execute(
            INSERT_QUERY,
            student["department"],
            student["stream"] if "stream" in student else "-",
            student["section"],
            student["name"],
            student["phone_number"],
            student["email"],
        )
        self._db.commit()

    def _create_table(self) -> None:
        self._db.execute(CREATE_TABLE_QUERY)
        self._db.commit()
