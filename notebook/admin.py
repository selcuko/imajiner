from django.contrib import admin

from .models import *


class NarrativeVersionInlineAdmin(admin.StackedInline):
    model = NarrativeVersion
    fields = ['version', 'title', 'body']
    readonly_fields = ['version', 'title', 'body']
    extra = 0
    max_num = 30
    classes = ['collapse']


class NarrativeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': ['author', 'created_at']}),
        ('Identifiers',       {'fields': ['uuid', 'slug']}),
    ]
    readonly_fields = ['author', 'created_at', 'uuid', 'slug']
    list_display = ['author', 'created_at']
    list_filter = ['sketch']

class NarrativeTranslationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': ['author']}),
        ('Identifiers',       {'fields': ['uuid', 'slug']}),
        ('Content',           {'fields': ['title', 'body', 'language']}),
        ('Generated Fields',  {'fields': ['html']}),
        ('Dates',             {'fields': ['published_at', 'created_at']}),
    ]
    readonly_fields = ['author', 'created_at', 'uuid', 'slug', 'html']
    list_display = ['title', 'language_display', 'sketch', 'edited_at']
    list_filter = ['sketch']

    def language_display(self, instance):
        return settings.LANGUAGES_DICT[instance.language] if settings.LANGUAGES_DICT.get(instance.language) else instance.language

    def author(self, instance):
        return instance.master.author.username

admin.site.register(Narrative, NarrativeAdmin)
admin.site.register(NarrativeTranslation, NarrativeTranslationAdmin)
