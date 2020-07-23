from django.db import models
from django.utils import text

class AbstractTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)



class TagManager(models.Model):
    def get(slug):
        return self.tags.get(slug=slug)


class ObjectTag(models.Model):
    abstract = models.ForeignKey(AbstractTag, on_delete=models.CASCADE, related_name='objects')
    count = models.IntegerField(default=1)
    manager = models.ForeignKey(TagManager, on_delete=models.CASCADE, related_name='tags')

