import logging
from dataclasses import asdict

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.pg_conn = pg_conn
        self.column_mapping = {
            "updated_at": "modified",
        }

    def save_data(self, table_name: str, data_batch: list):
        if not data_batch:
            return

        # 1. Берем поля из первого объекта батча
        sample_dict = asdict(data_batch[0])

        # 2. Формируем список колонок для SQL запроса, заменяя имена по маппингу
        pg_columns = [self.column_mapping.get(key, key) for key in sample_dict.keys()]
        cols_str = ", ".join(pg_columns)

        # 3. Подготавливаем кортежи значений
        values = [tuple(asdict(obj).values()) for obj in data_batch]

        # Укажите вашу схему (например, content)
        query = f"INSERT INTO content.{table_name} ({cols_str}) VALUES %s ON CONFLICT (id) DO NOTHING"

        try:
            with self.pg_conn.cursor() as cursor:
                execute_values(cursor, query, values)
                self.pg_conn.commit()
        except psycopg2.Error as e:
            self.pg_conn.rollback()
            logger.error(
                f"Ошибка Postgres при вставке в {table_name}: {e.pgcode} - {e.pgerror}",
            )
