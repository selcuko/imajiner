from django.contrib import admin
from django.db.models import Count

from .models import *



class NarrativeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'created_at']}),
        (None, {'fields': ['title', 'languages', 'uuid']})
    ]
    readonly_fields = ['title', 'uuid', 'created_at', 'languages']
    list_display = ['title', 'author', 'created_at']
    def get_queryset(self, *args, **kwargs):
        return Narrative.objects.prefetch_related('translations')



class NarrativeTranslationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': ['author']}),
        ('Identifiers',       {'fields': ['uuid', 'slug']}),
        ('Content',           {'fields': ['title', 'body', 'language']}),
        ('Generated Fields',  {'fields': ['html']}),
        ('Dates',             {'fields': ['published_at', 'created_at']}),
    ]
    readonly_fields = ['author', 'created_at', 'uuid', 'slug', 'html']
    list_display = ['title', 'author', 'language', 'sketch', 'versions', 'edited_at']
    list_filter = ['sketch', 'language']

    def language(self, instance):
        return settings.LANGUAGES_DICT.get(instance.language, instance.language)

    def author(self, instance):
        return instance.master.author.username
    
    def versions(self, instance):
        return instance.versions_count
    
    def get_queryset(self, *args, **kwargs):
        return NarrativeTranslation.objects.prefetch_related('versions').annotate(versions_count=Count('versions')).order_by('-edited_at', '-versions_count', 'sketch')
    

admin.site.register(Narrative, NarrativeAdmin)
admin.site.register(NarrativeTranslation, NarrativeTranslationAdmin)
