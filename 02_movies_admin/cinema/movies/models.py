import uuid

from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Person(TimeIDMixin, models.Model):
    full_name = models.CharField(
        _("ФИО"),
        validators=[MinLengthValidator(3)],
        max_length=200,
    )
    birth_date = models.DateField(_("День рождения"), null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:  # type: ignore
        verbose_name = _("Персона")
        verbose_name_plural = _("Персоны")
        db_table = '"content"."person"'

    def __str__(self):
        return self.full_name


class Genre(TimeIDMixin, models.Model):
    name = models.CharField(_("Название"), max_length=255)
    description = models.TextField(_("Описание"), blank=True, null=True)
    """В самой бд sqlite в 3-ей части урока в description есть значения null.
    При миграции возникает ошибка, если не разрешить null значения в моделях.
    Так же для стандартизации для пустых значений любого типа лучше null использовать, дабы
    избежать путаницы даже, если придётся хранить 2 типа значений
    """
    modified = models.DateTimeField(auto_now=True)

    class Meta:  # type: ignore
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")
        db_table = '"content"."genre"'

    def __str__(self):
        return self.name


class FilmworkGenre(TimeIDMixin, models.Model):
    filmwork = models.ForeignKey(
        "Filmwork",
        on_delete=models.CASCADE,
        to_field="id",
        db_column="film_work_id",
    )
    genre = models.ForeignKey(
        "Genre",
        on_delete=models.CASCADE,
        to_field="id",
        db_column="genre_id",
    )

    class Meta:  # type: ignore
        indexes = [
            models.UniqueConstraint(fields=["filmwork_id", "genre_id"], name="film_work_genre"),
        ]
        verbose_name = _("Жанр фильма")
        verbose_name_plural = _("Жанры фильмов")
        db_table = '"content"."genre_film_work"'

    def __str__(self):
        return str(f"{self.filmwork} - {self.genre}")


class PersonRole(TimeIDMixin, models.Model):
    class RoleType(models.TextChoices):
        ACTOR = "actor", _("актер")
        DIRECTOR = "director", _("директор")
        WRITER = "writer", _("сценарист")

    filmwork = models.ForeignKey(
        "Filmwork",
        on_delete=models.CASCADE,
        to_field="id",
        db_column="film_work_id",
    )
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        to_field="id",
        db_column="person_id",
    )
    role = models.CharField(
        _("role"),
        max_length=30,
        choices=RoleType.choices,
    )

    class Meta:  # type: ignore
        verbose_name = _("Роль и персона")
        verbose_name_plural = _("Роли и персоны")
        db_table = '"content"."person_film_work"'

        indexes = [
            models.UniqueConstraint(
                fields=["filmwork_id", "person_id", "role"],
                name="film_work_person_role",
            ),
        ]

    def __str__(self):
        return str(f"{self.filmwork} - {self.person}")


class Filmwork(TimeIDMixin, models.Model):
    class FilmworkType(models.TextChoices):
        MOVIE = "movie", _("фильм")
        TV_SHOW = "tv_show", _("ТВ шоу")

    title = models.CharField(_("Название"), max_length=255)
    description = models.TextField(_("Описание"), null=True, blank=True)
    creation_date = models.DateField(_("Дата выхода"), null=True, blank=True)
    certificate = models.TextField(_("certificate"), null=True, blank=True)
    file_path = models.FileField(
        _("Путь к файлу"),
        upload_to="film_works/",
        blank=True,
        null=True,
    )
    rating = models.FloatField(
        _("Рейтинг"),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0.0,
        null=True,
    )
    type = models.CharField(
        _("Тип произведения"),
        max_length=20,
        choices=FilmworkType.choices,
    )
    genres = models.ManyToManyField(Genre, through="FilmworkGenre")
    modified = models.DateTimeField(auto_now=True)

    class Meta:  # type: ignore
        verbose_name = _("Фильм")
        verbose_name_plural = _("Фильмы")
        db_table = '"content"."film_work"'

    def __str__(self):
        return self.title
