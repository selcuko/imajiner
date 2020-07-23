from django.db import models
from tagmanager.models import TagManager


class Narrative(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True)
    body = models.TextField(null=True)
    html = models.TextField(null=True)

    tagman = models.OneToOneField(TagManager, on_delete=models.SET_NULL, related_name='narrative', null=True)


