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
    inlines = [NarrativeVersionInlineAdmin]
    fieldsets = [
        (None,                {'fields': ['author']}),
        ('Identifiers',       {'fields': ['uuid', 'slug']}),
        ('Content',           {'fields': ['title', 'body']}),
        ('Generated Fields',  {'fields': ['html']}),
        ('Dates',             {'fields': ['published_at', 'created_at']}),
    ]
    readonly_fields = ['created_at', 'versions', 'author']
    empty_value_display = '???'
    

admin.site.register(Narrative, NarrativeAdmin)
