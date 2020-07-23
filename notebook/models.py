from django.db import models


class Narrative(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True)
    body = models.TextField(null=True)
    html = models.TextField(null=True)


