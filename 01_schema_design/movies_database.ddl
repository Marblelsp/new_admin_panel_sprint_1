CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work
(
    id            UUID PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT NOT NULL,
    created       TIMESTAMP WITH TIME ZONE,
    modified      TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre
(
    id          UUID PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created     TIMESTAMP WITH TIME ZONE,
    modified    TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           UUID PRIMARY KEY,
    genre_id     UUID NOT NULL
        CONSTRAINT genre_film_work_genre_id_fk
            REFERENCES content.genre,
    film_work_id UUID NOT NULL
        CONSTRAINT genre_film_work_film_work_id_fk
            REFERENCES content.film_work,
    created      TIMESTAMP WITH TIME ZONE
);

CREATE UNIQUE INDEX film_work_genre
    ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person
(
    id         UUID PRIMARY KEY,
    full_name  text NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           UUID PRIMARY KEY,
    person_id    UUID NOT NULL
        CONSTRAINT person_film_work_person_id_fk
            REFERENCES content.person,
    film_work_id UUID NOT NULL
        CONSTRAINT person_film_work_film_work_id_fk
            REFERENCES content.film_work,
    role         TEXT NOT NULL,
    created   TIMESTAMP WITH TIME ZONE
);

CREATE UNIQUE INDEX film_work_person_role
    ON content.person_film_work (film_work_id, person_id, role);
