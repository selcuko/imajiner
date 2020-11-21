from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NarrativeTranslation

@receiver(post_save, sender=NarrativeTranslation)
def create_tagman(sender, instance, created, **kwargs):
    if not created or instance.tags:
        return
    tagman = TagManager.objects.create()
    instance.tags = tagman
    instance.save(new_version=False)


@receiver(post_save, sender=NarrativeTranslation)
def update_tagman(sender, instance, **kwargs):
    instance.tags.save()