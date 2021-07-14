from django.contrib import admin

from .models import Language, Snippet


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Snippet)
