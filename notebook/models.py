from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from tagmanager.models import TagManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import text, html
from uuid import uuid1
from django.utils import timezone

class SoundRecord(models.Model):
    file = models.FileField(
        upload_to='voice-records',
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'aac', 'wav', 'opus'])],
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
    versioning = models.BooleanField(default=True, verbose_name='Keeps seperate versions')
    title = models.CharField(max_length=100, default='Başlıklı hikaye', verbose_name='Title')
    slug = models.SlugField(max_length=100, null=True, unique=True, verbose_name='Slug')
    body = models.TextField(null=True, verbose_name='Body')
    html = models.TextField(null=True, verbose_name='HTML')
    sketch = models.BooleanField(default=False, verbose_name='Sketch')
    uuid = models.UUIDField(verbose_name='UUID')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='narratives', null=True)
    tags = models.OneToOneField(TagManager, on_delete=models.SET_NULL, related_name='narrative', null=True)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Publication date')

    class Meta:
        ordering = ('created_at',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.uuid: self.uuid = uuid1()
    
    def all_versions(self):
        return self.versions.all()
    
    @property
    def latest(self):
        return self.versions.first()

    @property
    def published(self):
        return bool(self.published_at)

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
        return f'"{self.title}" by {self.author.username}'
    
    def get_absolute_url(self):
        if self.sketch:
            return reverse('narrative:sketch', kwargs={'uuid': self.uuid})
        else:
            return reverse('narrative:detail', kwargs={'slug': self.slug})
    
    def generate_html(self):
        self.html = html.escape(self.body)
        self.html = self.html.replace('\n\n', '<br />')
        self.html = self.html.replace('\n', '</p><p>')
        self.html = f'<p>{self.html}</p>'

    def save(self, *args, alter_slug=True, new_version=False, **kwargs):
        self.generate_html()
        if alter_slug: self.generate_slug()
        if not self.published_at and not self.sketch:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)

        initial_version = self.versions.count() == 0
        if new_version:
            self.latest.archive()
            latest = NarrativeVersion(master=self)
            latest.reference(self)
            v = self.latest.version + 1 if not initial_version else 1
            latest.version = v
            self.version = latest.version
        else:
            latest = self.versions.last() if not initial_version else NarrativeVersion(master=self, version=1)
            latest.reference(self)
        latest.save()
    
    @property
    def lead(self):
        if not self.html: return 'SQL yine coşturmuş'
        p = self.html.split('</p><p>')
        return p[0].replace('<p class="drop-cap">', '').replace('</p>', '').replace('<p>', '')
    
    def generate_slug(self):
        self.slug = f'{text.slugify(self.title, allow_unicode=False)}-{str(self.uuid)[:8]}'

@receiver(post_save, sender=Narrative)
def create_tagman(sender, instance, created, **kwargs):
    """Create TagManager for Narrative programmatically."""

    if not created or instance.tags:
        return
    tagman = TagManager.objects.create()
    instance.tags = tagman
    instance.save(new_version=False)

@receiver(post_save, sender=Narrative)
def update_tagman(sender, instance, **kwargs):
    instance.tags.save()


class NarrativeVersion(models.Model):
    readonly = models.BooleanField(default=False)
    title = models.CharField(max_length=100, default='Başlıklı hikaye')
    slug = models.SlugField(max_length=100, null=True, unique=True)
    body = models.TextField(null=True)
    html = models.TextField(null=True)
    sketch = models.BooleanField(default=False)
    uuid = models.UUIDField()
    sound = models.ForeignKey(SoundRecord, null=True, blank=True, on_delete=models.SET_NULL, related_name='narratives')
    version = models.PositiveIntegerField(default=1)
    master = models.ForeignKey(Narrative, on_delete=models.CASCADE, related_name='versions')
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.uuid: self.uuid = uuid1()

    def __str__(self):
        return f'v{self.version}: {self.title}'

    def reference(self, ref):
        self.title = ref.title
        self.body = ref.body
        self.html = ref.html
        self.sketch = ref.sketch
        self.master = ref
    
    def assign_version(self, ref=None):
        self.version = 1
    
    def archive(self):
        return self.save(archive=True)

    def save(self, archive=False, overwrite=False, *args, **kwargs):
        if self.readonly and not overwrite:
            raise Exception('This version is read-only.')
        self.readonly = archive
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-version',)