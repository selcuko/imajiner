import logging
import inspect
from datetime import datetime
from threading import Thread
from uuid import uuid1

import cld3
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.shortcuts import reverse
from django.utils import html, text, timezone
from django.utils.functional import cached_property
from tagmanager.models import TagManager
from .methods import generate


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
                             max_length=100, default='', verbose_name='Title')
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
            if len(self.body) > self.LANG_MIN_LEN:
                cleaned = generate.clean(self.body)
                language = cld3.get_language(cleaned)
                if language.is_reliable and language in settings.LANGUAGES_DICT.keys():
                    self.language = language.language
            elif user_language:
                self.language = user_language
        self.is_published = not self.sketch
        self.edited_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.uuid:
            self.uuid = uuid1()


class Narrative(Base):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='narratives', null=True, blank=True)

    class Meta:
        ordering = ('author',)
    
    @cached_property
    def is_published(self):
        return self.translations.filter(is_published=True).exists()
    
    @cached_property
    def edited_at(self):
        qs = self.translations.order_by('-edited_at')
        if qs.exists():
            return qs.first().edited_at
    
    @cached_property
    def published_at(self):
        qs = self.translations.filter(published_at__isnull=False).order_by('-published_at')
        if qs.exists():
            return qs.first().published_at

    @cached_property
    def title(self):
        for t in self.translations.all():
            if t.title:
                return t.title
        return None

    @cached_property
    def languages_available(self):
        return [t.language for t in self.translations.all()]

    @property
    def languages_available_verbose(self, seperator=' • '):
        return seperator.join([str(settings.LANGUAGES_DICT.get(l, l)) for l in self.languages_available if l])

    @cached_property
    def languages_available_count(self):
        return self.translations.count()

    def __str__(self):
        return self.title if self.title else ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.language in self.languages_available:
            nt = self.translations.get(language=self.language)
            nt.reference(self)
            nt.save()

    def get_absolute_url(self):
        if self.sketch:
            return reverse('narrative:sketch', kwargs={'uuid': self.uuid})
        else:
            return reverse('narrative:detail', kwargs={'slug': self.slug})


class NarrativeTranslation(Base):
    master = models.ForeignKey(
        Narrative, on_delete=models.CASCADE, related_name='translations')
    tags = models.OneToOneField(
        TagManager, on_delete=models.SET_NULL, related_name='narrative', null=True)
    edited = models.BooleanField(default=False)

    @property
    def at_version(self):
        return self.versions.filter(sketch=False).count()
    @property
    def latest(self):
        return self.versions.filter(sketch=False).first()

    def get_absolute_url(self):
        if self.sketch:
            return reverse('narrative:sketch', kwargs={'uuid': self.uuid})
        else:
            return reverse('narrative:detail', kwargs={'slug': self.slug})

    def reference(self, ref):
        self.title = ref.title
        self.body = ref.body
        self.language = ref.language
        self.master = ref
        self.sketch = ref.sketch


    def save(self, *args, new_version=True, **kwargs):
        super().save(*args, **kwargs)

        initial_version = self.versions.count() == 0
        latest = self.versions.first()  # versions are ordered from latest to earliest
        if latest is not None:
            if latest.is_published:
                self.edited = True

        if initial_version:
            nv = NarrativeVersion()
            nv.reference(self)
            nv.version = 0
            nv.save()
        
        elif self.is_published and not new_version:
            #  gotta be an edit after the publish
            if not latest.sketch:
                latest = self.versions.filter(sketch=True).first()
            if not latest:
                latest = NarrativeVersion()
                latest.version = self.versions.first().version + 1
            latest.reference(self)
            latest.sketch = True
            latest.save()

        elif new_version:
            # save a new version and archive latest
            nv = NarrativeVersion()
            nv.reference(self)
            nv.version = latest.version + 1 if not self.is_published else 0
            nv.save()
            # latest.reference(self)
            latest.sketch = False
            latest.save(archive=True)
            self.edited = False

        else:
            # update latest version without creating a new one
            latest.reference(self)
            latest.save()
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{settings.LANGUAGES_DICT.get(self.language, "Unknown")} translation of {self.master}'


class NarrativeVersion(Base):
    readonly = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)
    master = models.ForeignKey(
        NarrativeTranslation, on_delete=models.CASCADE, related_name='versions')

    def __str__(self):
        return f'v{self.version}: {self.title}'

    def reference(self, ref):
        self.title = ref.title
        self.body = ref.body
        self.sketch = ref.sketch
        self.master = ref
        self.language = ref.language
        self.is_published = ref.is_published

    def archive(self):
        return self.save(archive=True)

    def save(self, *args, archive=False, overwrite=False, silent=True, **kwargs):
        if self.readonly and not overwrite:
            if not silent:
                raise Exception(f'This version is read-only: {self.title}')
            logger.error(f'This version is read-only: {self.title}')
        if archive:
            self.readonly = True
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-version',)
