import sqlite3


class SqliteDb:
    def __init__(self, connection_string: str) -> None:
        self._connection = sqlite3.connect(connection_string)
        self._cursor = self._connection.cursor()

    def create_table(self, table_name: str, columns: list[str]) -> None:
        self.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")
        self.commit()

    def execute(self, query: str, *args: object) -> None:
        self._cursor.execute(query, args)

    def query(self, query: str, *args: object) -> list:
        self._cursor.execute(query, args)
        return self._cursor.fetchall()

    def commit(self) -> None:
        self._connection.commit()

    def __del__(self) -> None:
        self._connection.close()
