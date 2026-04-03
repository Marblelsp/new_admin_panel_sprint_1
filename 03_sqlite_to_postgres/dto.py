import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime
    file_path: str


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class GenreFilmWork:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    id: uuid.UUID
    created_at: datetime


@dataclass(frozen=True)
class Person:
    id: uuid.UUID
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PersonFilmWork:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    id: uuid.UUID
    role: str
    created_at: datetime
