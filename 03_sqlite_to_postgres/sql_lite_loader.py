import sqlite3


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    def load_data(self, table_name: str, model_class, batch_size=100):
        """Читает данные из SQLite и возвращает генератор с объектами dataclass"""
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield [model_class(**dict(row)) for row in rows]
