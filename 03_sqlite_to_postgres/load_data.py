import sqlite3

import psycopg2
from config import dsl
from dto import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from postgres_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sql_lite_loader import SQLiteLoader


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных"""
    sqlite_loader = SQLiteLoader(connection)
    postgres_saver = PostgresSaver(pg_conn)

    tables = [
        ("film_work", FilmWork),
        ("genre", Genre),
        ("person", Person),
        ("genre_film_work", GenreFilmWork),
        ("person_film_work", PersonFilmWork),
    ]

    for table_name, model in tables:
        for batch in sqlite_loader.load_data(table_name, model):
            postgres_saver.save_data(table_name, batch)


if __name__ == "__main__":
    with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg2.connect(
        **dsl,
        cursor_factory=DictCursor,
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
