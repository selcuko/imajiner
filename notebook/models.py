from django.db import models
from django.core.exceptions import ValidationError
from tagmanager.models import TagManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import text, html
from uuid import uuid1 as uuid


def ext_validator(file):
        valid = ['mp3', 'aac', 'wav', 'opus']
        if file.name.split('.')[-1] not in valid:
            raise ValidationError('File extension invalid. Options:', str(valid))

class SoundRecord(models.Model):
    file = models.FileField(
        upload_to='voice-records',
        validators=[ext_validator]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self):
        return f'Voice record file {self.file.name} at {self.uploaded_at}'

    def save(self, *args, **kwargs):
        if not self.uploader: raise Exception('SoundRecord with no uploader user.')
        super().save(*args, **kwargs)


class Narrative(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, unique=True)
    body = models.TextField(null=True)
    html = models.TextField(null=True)
    sketch = models.BooleanField(default=False)
    uuid = models.UUIDField()
    sound = models.OneToOneField(SoundRecord, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='narratives', null=True)
    tags = models.OneToOneField(TagManager, on_delete=models.SET_NULL, related_name='narrative', null=True)

    class Meta:
        ordering = ('created_at',)
    
    @classmethod
    def viewable(cls, user):
        if isinstance(user, str):
            user = User.objects.get(username=user)
        elif isinstance(user, User):
            pass
        else:
            raise Exception('Invalid argument supplied')
        
        return cls.objects.filter(author=user, sketch=False)

    def __str__(self):
        return f'{self.title} ({self.slug})'
    
    def get_absolute_url(self):
        if self.sketch:
            return reverse('narrative:sketch', kwargs={'slug': self.slug})
        else:
            return reverse('narrative:detail', kwargs={'slug': self.slug})
    
    def save(self, *args, alter_slug=True, **kwargs):
        self.html = html.escape(self.body)
        self.html = self.html.replace('\n\n', '<br />')
        self.html = self.html.replace('\n', '</p><p>')
        self.html = f'<p class="drop-cap">{self.html}</p>'
        if not self.uuid: self.uuid = uuid()
        if alter_slug:
            self.generate_slug()
        super().save(*args, **kwargs)
    
    @property
    def lead(self):
        if not self.html: return 'SQL yine coşturmuş'
        p = self.html.split('</p><p>')
        return p[0].replace('<p class="drop-cap">', '').replace('</p>', '')
    
    def generate_slug(self):
        if not self.uuid: self.uuid = uuid()
        self.slug = f'{text.slugify(self.title, allow_unicode=False)}-{str(self.uuid)[:8]}'

@receiver(post_save, sender=Narrative)
def create_tagman(sender, instance, created, **kwargs):
    """Create TagManager for Narrative programmatically."""

    if not created or instance.tags:
        return
    tagman = TagManager.objects.create()
    instance.tags = tagman
    instance.save()

@receiver(post_save, sender=Narrative)
def update_tagman(sender, instance, **kwargs):
    instance.tags.save()




