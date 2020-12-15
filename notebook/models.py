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
from .exceptions import AbsentMasterException, ReadonlyException
from . import managers

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class Base(models.Model):
    LANG_MIN_LEN = 40

    class Meta:
        abstract = True
        ordering = ('-published_at', '-created_at')

    title = models.CharField(
        null=True, 
        blank=True,
        max_length=100, 
        verbose_name='Title')
    body = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='Body')
    raw = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='Raw Text')
    lead = models.TextField(
        null=True, 
        blank=True, 
        verbose_name='Summary')
    html = models.TextField(
        null=True, 
        verbose_name='HTML')
    slug = models.SlugField(
        max_length=100, 
        null=True,
        unique=True, 
        verbose_name='Slug')
    uuid = models.UUIDField(
        unique=True,
        verbose_name='UUID')
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Creation date')
    published_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Publication date')
    edited_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Last edited at')
    language = models.CharField(
        max_length=5, 
        null=True, 
        blank=True, 
        choices=settings.LANGUAGES)
    sketch = models.BooleanField(default=True)
    public = models.BooleanField(null=True, blank=True)


    @property
    def is_published(self):
        return bool(self.published_at)

    def save(self, *args, **kwargs):
        if isinstance(self.title, str) and len(self.title) is 0:
            self.title = None
        if isinstance(self.body, str) and len(self.body) is 0:
            self.body = None
        if not self.sketch or kwargs.pop('generate', False):
            if self.body:
                self.html = generate.html(self.body)
                self.raw = generate.raw(self.html)
                
        if self.raw and kwargs.pop('update_lead', True):
            self.lead = generate.lead(self.raw)

        if self.title and kwargs.pop('update_slug', True):
            self.slug = generate.slug(self.title, uuid=self.uuid)

        if not self.published_at and not self.sketch:
            self.published_at = timezone.now()

        if not self.sketch or kwargs.pop('update_language', False):
            if self.body and len(self.body) > self.LANG_MIN_LEN:
                cleaned = generate.clean(self.body)
                result = cld3.get_language(cleaned)
                logger.debug(f'NarrativeTranslation language classification results: {result}')
                if result.is_reliable:
                    language = result.language.split('-')[0][:5]
                    self.language = language
                else:
                    logger.debug(f'NarrativeTranslation failed language classification.')

            else:
                logger.debug(f'NarrativeTranslation skipped language classification.')

        super().save(*args, **kwargs)

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
    uuid = models.UUIDField(
        unique=True,
        verbose_name='UUID')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def title(self):
        for t in self.translations.all():
            if t.title:
                return t.title
        return None
    
    @property
    def is_published(self):
        return bool(self.published_at)

    @property
    def edited_at(self):
        try:
            return self.translations.order_by('-edited_at').first().edited_at
        except:
            return

    @property
    def published_at(self):
        try:
            return self.translations.order_by('-created_at').first().published_at
        except:
            return

    @property
    def languages(self):
        return [t.language for t in self.translations.all()]
    
    def __str__(self):
        if self.title: return self.title
        else: return ''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.uuid:
            self.uuid = uuid1()

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
    objects = managers.NarrativePublicity()


    def autosave(self, *args, **kwargs):
        """Autosave given instance. If possible, 
        updates the latest version. Otherwise creates a new NarrativeVersion. 

        Returns:
            NarrativeVersion: latest and saved version of given instance
        """

        self.save(*args, **kwargs)
        if (self.latest is None) or self.latest.readonly:
            nv = NarrativeVersion()
        else:
            nv = self.latest
        nv.reference(self, autosave=True, sketch=True, is_published=False)
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
        self.save(*args, **kwargs)

        if self.latest is None:
            self.autosave(*args, **kwargs)
        
        nv = NarrativeVersion() if self.latest.readonly else self.latest
        nv.reference(self)
        nv.save(archive=True)
        return self.latest

    @property
    def latest(self):
        return self.versions.first()
    
    @property
    def published(self):
        self.versions.filter(sketch=False).first()

    @property
    def version(self):
        # latest published version
        # TODO: this function seems to lack something
        return self.versions.filter(sketch=False).first().version if self.versions.count() is not 0 else None

    def get_absolute_url(self):
        if self.sketch:
            return reverse('narrative:sketch', kwargs={'uuid': self.uuid})
        else:
            return reverse('narrative:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        try:
            if not self.master.pk:  # check whether instance has a master
                pass
            kwargs.pop('author', None)  # remove item to avoid passing to super().save()
            
        except NarrativeTranslation.master.RelatedObjectDoesNotExist:
            author = kwargs.pop('author', None)
            if author:
                master = Narrative(author=author)
                master.save()
                self.master = master
            else:
                raise AbsentMasterException(self)
        
        super().save(*args, **kwargs)

        nv = self.latest if self.latest else NarrativeVersion()
        nv.reference(self, autosave=True)
        nv.save(overwrite=True)


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

    def reference(self, point, **kwargs):
        autosave = kwargs.pop('autosave', False)
        overwrite = kwargs.pop('overwrite', False)
        save = kwargs.pop('save', False)
        self.master = point if 
        self.title = point.title
        self.body = point.body
        self.sketch = point.sketch if not overwrite else True
        self.is_published = kwargs.pop('is_published') if kwargs.get('is_published') else point.is_published 
        self.language = point.language

        if point.latest is not None:
            self.version = point.latest.version
            if not autosave: self.version += 1
        else:
            self.version = 0
        
        if save:
            self.save(overwrite=overwrite, **kwargs)

    def archive(self):
        return self.save(archive=True)

    def save(self, *args, **kwargs):
        silent = kwargs.pop('silent', False)
        overwrite = kwargs.pop('overwrite', False)

        if self.readonly and not overwrite:
            logger.error(str(ReadonlyException(self)))
            if not silent:
                raise ReadonlyException(self)

        if kwargs.pop('archive', False):
            self.readonly = True
        super().save(*args, **kwargs)

