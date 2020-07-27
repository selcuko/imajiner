from django.db import models
from tagmanager.models import TagManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse


class Narrative(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True)
    body = models.TextField(null=True)
    html = models.TextField(null=True)

    tagman = models.OneToOneField(TagManager, on_delete=models.SET_NULL, related_name='narrative', null=True)

    def __str__(self):
        return f'{self.title} ({self.slug})'
    
    def get_absolute_url(self):
        return reverse('narrative:detail', kwargs={'slug': self.slug})

@receiver(post_save, sender=Narrative)
def create_tagman(sender, instance, created, **kwargs):
    """Create TagManager for Narrative programmatically."""

    if not created or instance.tagman:
        return
    tagman = TagManager.objects.create()
    instance.tagman = tagman
    instance.save()

@receiver(post_save, sender=Narrative)
def update_tagman(sender, instance, **kwargs):
    instance.tagman.save()




