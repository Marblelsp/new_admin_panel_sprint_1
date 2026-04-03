from django.contrib import admin

from .models import Filmwork, FilmworkGenre, Genre, Person, PersonRole

ROWS_PER_PAGE = 20
"""Количество строк на страницу"""


class GenreInline(admin.TabularInline):
    model = FilmworkGenre
    extra = 0
    verbose_name = "Жанр"
    autocomplete_fields = ("genre",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("genre", "filmwork")


class PersonRoleInline(admin.TabularInline):
    model = PersonRole
    extra = 0
    verbose_name = "Роль"
    autocomplete_fields = ("person",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("person", "filmwork")


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_filter = ("type",)
    search_fields = ("title", "description", "id")
    list_display = ("title", "type", "creation_date", "rating", "get_genres")
    fields = (
        "title",
        "type",
        "description",
        "creation_date",
        "certificate",
        "file_path",
        "rating",
    )

    list_prefetch_related = ("genres",)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])



    empty_value_display = "-пусто-"
    inlines = [
        GenreInline,
        PersonRoleInline,
    ]
    ordering = ("title",)
    list_per_page = ROWS_PER_PAGE

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "birth_date", "id")
    list_display = (
        "full_name",
        "birth_date",
        "created_at",
        "modified",
    )
    empty_value_display = "-пусто-"
    ordering = ("full_name",)
    list_per_page = ROWS_PER_PAGE


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "description",
        "created_at",
        "modified",
    )
    empty_value_display = "-пусто-"
    ordering = ("name",)
    list_per_page = ROWS_PER_PAGE
