from django.db import models
from django.db.models import Q


class NarrativePublicity(models.Manager):

    def public(self, *args, **kwargs):
        """Returns all publicly browsable instanes
        of given QuerySet.

        Returns:
            QuerySet: Publicly viewable instances
        """

        visitor = kwargs.pop('visitor', None)
        qs = super().all().exclude(
            Q(sketch=True) |
            Q(language__isnull=True) | 
            Q(title__isnull=True) | 
            Q(title__exact='') |
            Q(body__isnull=True) | 
            Q(body__exact='') |
            Q(master__isnull=True)
            )
        return qs
    

    def sketches(self, *args, **kwargs):
        """Returns sketches that belongs to a particular author.

        Args:
            author (auth.User): Author

        Returns:
            QuerySet: Sketches of the author
        """

        author = kwargs.pop('author')
        qs = super().filter(
            master__author=author,
            sketch=True,
        )
        return qs
    
    
    def sketch(self, *args, **kwargs):
        """Returns a particular sketch of an author.

        Args:
            author (auth.User): Author of the sketch
            uuid (UUID): UUID of sketch to be returned

        Returns:
            NarrativeTranslation: Sketch of that author
        """

        uuid = kwargs.pop('uuid')
        return self.sketches(*args, **kwargs).get(uuid=uuid)
    

    def of(self, *args, **kwargs):
        """All public narratives of an author.

        Args:
            author (auth.User): The author

        Returns:
            QuerySet: All published narratives of the author
        """
        author = kwargs.pop('author')
        return self.public(*args, **kwargs).filter(master__author=author)