from django.db import models


class NarrativePublicity(models.Manager):

    def public(self, *args, **kwargs):
        visitor = kwargs.pop('visitor', None)
        qs = super().filter(
            sketch=False,
            language__isnull=False,
            title__isnull=False,
            body__isnull=False)
        return qs
    
    def sketches(self, *args, **kwargs):
        author = kwargs.pop('author')
        qs = super().filter(
            master__author=author,
            sketch=True,
        )
        # qs.filter(title__isnull=True, body__isnull=True).delete()
        return qs
    
    def sketch(self, *args, **kwargs):
        uuid = kwargs.pop('uuid')
        return self.sketches(*args, **kwargs).get(uuid=uuid)