from typing import Annotated, TypedDict

Section = Annotated[str, "Section"]

SERVICE_DEPARTMENTS = [
    "ጽህፈት ቤት",
    "ሰንበት ኦዲት እና ኢንስፔሽን ክፍል",
    "አባላት እንክብካቤ ምክክር እና አቅም ማጎልበቻ",
    "ትምህርት ክፍል",
    "ሙያ እና በጎ አድራጎት ክፍል",
    "ባች እና መርሐ ግብራት ማስተባበሪያ ክፍል",
    "መዝሙር እና ሥነ-ጥበባት ክፍል",
    "ልማት እና ገቢ አሰባሰብ ክፍል",
    "ሒሳብ እና ንብረት ክፍል",
    "እቅድ ክትትል ሪፖርት እና መረጃ ማደራጃ ክፍል",
    "ቋንቋ እና ልዩ ፍላጎት ክፍል",
]


class Stream(TypedDict):
    name: str
    abbreviation: str
    sections: list[Section]


class Department(TypedDict):
    name: str
    abbreviation: str
    sections: list[Section]
    streams: list[Stream]


class Student(TypedDict):
    name: str
    phone_number: str
    email: str
    department: str
    stream: str
    section: str
    service_department: str


DEPARTMENTS: list[Department] = [  # type: ignore
    {
        "name": "School of Information Technology and Engineering",
        "abbreviation": "SITE",
    },
    {"name": "School of Electrical and Computer Engineering", "abbreviation": "SECE"},
    {"name": "School of Chemical and Bio Engineering", "abbreviation": "SCBE"},
    {"name": "School of Civil and Environmentall Engineering", "abbreviation": "SCEE"},
    {"name": "School of Mechanical and Industrial Engineering", "abbreviation": "SMIE"},
    {"name": "School of Center of Biomedical Engineering", "abbreviation": "SCBE"},
]


def get_departments() -> list[Department]:
    return DEPARTMENTS


def get_department_names() -> list[str]:
    return [department["name"] for department in get_departments()]


def get_department_streams(department_name: str) -> list[Stream]:
    for department in DEPARTMENTS:
        if department["name"] == department_name:
            if "streams" in department:
                return department["streams"]

    return []


def get_department_stream_names(department_name: str) -> list[str]:
    streams = get_department_streams(department_name)
    return [stream["name"] for stream in streams]


def get_sections(department_name: str, stream_name: str | None = None) -> list[Section]:
    for department in DEPARTMENTS:
        if department["name"] == department_name:
            if not stream_name:
                return department["sections"]  # type: ignore

            for stream in department["streams"]:  # type: ignore
                if stream["name"] == stream_name:
                    return stream["sections"]  # type: ignore

    return []
