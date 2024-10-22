from formbot.bot.forms.y2024.fifth_year_form.form_resources import Student
from formbot.storage import SqliteDb

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    service_department TEXT,
    department TEXT,
    stream TEXT,
    section TEXT
)
"""

INSERT_QUERY = """
INSERT INTO students (name, phone, email, service_department, department, stream, section) VALUES (?, ?, ?, ?, ?, ?, ?);
"""


class FormService:
    def __init__(self) -> None:
        self._db = SqliteDb("./data/fifth_year_2024_form.db")
        self._create_table()

    def insert(self, student: Student) -> None:
        self._db.execute(
            INSERT_QUERY,
            student["name"],
            student["phone_number"],
            student["email"],
            student["service_department"],
            student["department"] if "department" in student else "-",
            student["stream"] if "stream" in student else "-",
            student["section"] if "section" in student else "-",
        )
        self._db.commit()

    def fetch(self) -> list[Student]:
        self._db.query("SELECT * FROM students")

        return []

    def _create_table(self) -> None:
        self._db.execute(CREATE_TABLE_QUERY)
        self._db.commit()
