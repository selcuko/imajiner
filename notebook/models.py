import inspect
import logging
from datetime import datetime
from threading import Thread
from uuid import uuid1

import cld3
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Count
from django.shortcuts import reverse
from django.utils import html, text, timezone
from django.utils.functional import cached_property
from tagmanager.models import TagManager

from .methods import generate
from .exceptions import AbsentMasterException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SoundRecord(models.Model):
    file = models.FileField(
        upload_to='voice-records',
        validators=[FileExtensionValidator(
            allowed_extensions=['mp3', 'aac', 'wav', 'opus'])],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Voice record file {self.file.name} at {self.uploaded_at}'

    def save(self, *args, **kwargs):
        if not self.uploader:
            raise Exception('SoundRecord with no uploader user.')
        super().save(*args, **kwargs)

class Base(models.Model):
    LANG_MIN_LEN = 40

    class Meta:
        abstract = True
        ordering = ('-published_at', '-created_at')

    title = models.CharField(null=True, blank=True,
                             max_length=100, verbose_name='Title')
    body = models.TextField(null=True, verbose_name='Body')
    raw = models.TextField(null=True, blank=True, verbose_name='Raw')
    lead = models.TextField(null=True, blank=True, verbose_name='Summary')
    html = models.TextField(null=True, verbose_name='HTML')
    slug = models.SlugField(max_length=100, null=True,
                            unique=True, verbose_name='Slug')
    uuid = models.UUIDField(verbose_name='UUID', unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creation date')
    published_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Publication date')
    edited_at = models.DateTimeField(
        auto_now=True, verbose_name='Last edited at')
    language = models.CharField(
        max_length=5, null=True, blank=True, choices=settings.LANGUAGES)
    sketch = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    public = models.BooleanField(null=True, blank=True)

    def save(self, *args, alter_slug=True, update_lead=True, user_language=None, **kwargs):
        if not self.sketch:
            self.html = generate.html(self.body)
            self.raw = generate.raw(self.html)
            if update_lead:
                self.lead = generate.lead(self.raw)
            if alter_slug:
                self.slug = generate.slug(self.title, uuid=self.uuid)
        if not self.published_at and not self.sketch:
            self.published_at = timezone.now()

        if not self.sketch:
            logger.debug(f'NarrativeTranslation ({self.title}) available for language classification.')
            if len(self.body) > self.LANG_MIN_LEN:
                cleaned = generate.clean(self.body)
                result = cld3.get_language(cleaned)
                logger.debug(f'NarrativeTranslation language classification results: {result}')
                if result.is_reliable:
                    language = result.language.split('-')[0][:5]
                    self.language = language
            elif user_language:
                logger.debug(f'NarrativeTranslation.body too short for language classification but user-language supplied instead.')
                self.language = user_language
            else:
                logger.debug(f'NarrativeTranslation did not fit in any case for language classification.')
        self.is_published = not self.sketch
        self.edited_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.uuid:
            self.uuid = uuid1()


class Narrative(models.Model):
    class Meta:
        ordering = ('author',)

    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='narratives', 
        null=True, 
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def title(self):
        for t in self.translations.all():
            if t.title:
                return t.title
        return None


        return self.translations.count()

    def __str__(self):
        return self.title if self.title else ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class NarrativeTranslation(Base):
    class Meta(Base.Meta):
        ordering = ('-edited_at', 'edited_at')

    master = models.ForeignKey(
        Narrative, 
        on_delete=models.CASCADE, 
        related_name='translations')
    tags = models.OneToOneField(
        TagManager, 
        on_delete=models.SET_NULL, 
        related_name='narrative', 
        null=True)
    edited = models.BooleanField(default=False)


    def autosave(self, *args, **kwargs):
        """Autosave given instance. If possible, 
        updates the latest version. Otherwise creates a new NarrativeVersion. 

        Returns:
            NarrativeVersion: latest and saved version of given instance
        """
        self.save()
        if self.latest is None or self.latest.readonly:
            nv = NarrativeVersion()
        else:
            nv = self.latest
        nv.reference(self)
        nv.save()
        return self.latest

    def publish(self, *args, **kwargs):
        """Publishes given instance's latest version. If readonly,
        creates a new NarrativeVersion referencing instance and publishes
        that.

        Returns:
            NarrativeVersion: latest and saved version of given instance
        """

        self.sketch = False
        self.save()

        if self.latest is None:
            self.autosave()
        
        nv = NarrativeVersion() if self.latest.readonly else self.latest
        nv.reference(self)
        nv.save()
        return self.latest

    @property
    def latest(self):
        return self.versions.first()
    
    @property
    def at_version(self):
        # latest published version
        # TODO: this function seems to lack something
        return self.versions.filter(sketch=False).count()

    def get_absolute_url(self):
        if self.sketch:
            return reverse('narrative:sketch', kwargs={'uuid': self.uuid})
        else:
            return reverse('narrative:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        try:
            author = kwargs.get('author')
            if author:
                self.master = Narrative(author=author)
                self.master.save()
        except NarrativeTranslation.master.RelatedObjectDoesNotExist:
            raise AbsentMasterException('This instance of NarrativeTranslation has no master and no author is supplied')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)



class NarrativeVersion(Base):
    class Meta:
        ordering = ('-version',)
    
    readonly = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)
    master = models.ForeignKey(
        NarrativeTranslation, 
        on_delete=models.CASCADE, 
        related_name='versions')

    def __str__(self):
        return f'v{self.version}: {self.title}'

    def reference(self, ref):
        self.master = ref
        self.title = ref.title
        self.body = ref.body
        self.sketch = ref.sketch
        self.language = ref.language
        self.is_published = ref.is_published
        self.version = ref.latest.version + 1 if ref.latest is not None else 1

    def archive(self):
        return self.save(archive=True)

    def save(self, *args, **kwargs):
        silent = kwargs.get('silent', True)
        overwrite = kwargs.get('overwrite')

        if self.readonly and not overwrite:
            if not silent:
                raise ReadonlyException(self)
            logger.error(str(ReadonlyException(self)))

        if kwargs.get('archive'):
            self.readonly = True
        super().save(*args, **kwargs)

